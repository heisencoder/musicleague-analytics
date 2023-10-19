"""Flattened model representation of Music League export merged with Spotify data """

from collections import defaultdict
import csv

from pydantic import BaseModel

from src import csv_model
from src import spotify


VOTE_CAP_POINTS = 2  # Highest number of points to assign for cap_points


class FlatVote(BaseModel):
    """A flattened version of a Vote or Submission"""

    round_id: str  # Round.ID
    round_name: str  # Foreign key to Round.Name
    voter_id: str  # Competitor.ID
    voter_name: str  # Foreign key to Competitor.Name
    track_uri: str  # Spotify Track URI
    track_name: str  # Name of Spotify track
    track_artists: str  # semicolon-joined list of artist names on track
    points: int  # Number of points given to song by voter. Self-submissions included
    cap_points: int  # Number of points but with a capped vote
    is_submitter: bool  # Whether this person submitted the song
    track_genres: str  # semicolon-joined list of genres of artists on the track


def get_track_dict(track: spotify.Track) -> dict[str, str]:
    """Returns a dict that contains track fields of a FlatVote"""
    # pylint: disable=locally-disabled, use-dict-literal
    track_genres: set[str] = set()
    for artist in track.artists:
        assert artist.genres is not None
        track_genres.update(artist.genres)
    return dict(
        track_uri=track.uri,
        track_name=track.name,
        track_artists=";".join([a.name for a in track.artists]),
        track_genres=";".join(sorted(track_genres)),
    )


def get_missing_votes(
    votes: list[FlatVote],
    competitors: dict[str, str],
    rounds: dict[str, str],
    tracks: dict[str, spotify.Track],
) -> list[FlatVote]:
    """Find implicit zero votes and fill-in an explicit vote of zero points.

    Note that this also requires identifying who did not participate in a particular round,
    either due to not submitting a song in time, or not submitting votes in time, and
    not providing zero votes for them.
    """

    missing_votes = []
    # First, figure out who voted in a given round. Each participant must have voted
    # at least one time, due to needing to spend all points.

    round_voters = defaultdict(set)  # dict of RoundIDs to set of VoterIDs
    round_songs = defaultdict(set)  # dict of RoundIDs to set of track SpotifyURI
    round_song_voters: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )  # dict of roundIDs to dict of SpotifyURI to set of VoterIDS

    for vote in votes:
        round_song_voters[vote.round_id][vote.track_uri].add(vote.voter_id)
        if vote.is_submitter:
            continue
        round_voters[vote.round_id].add(vote.voter_id)
        round_songs[vote.round_id].add(vote.track_uri)

    for round_id in round_voters:
        for track_uri in round_songs[round_id]:
            missing_voters = (
                round_voters[round_id] - round_song_voters[round_id][track_uri]
            )
            for missing_voter in missing_voters:
                blank_vote = FlatVote(
                    round_id=round_id,
                    round_name=rounds[round_id],
                    voter_id=missing_voter,
                    voter_name=competitors[missing_voter],
                    **get_track_dict(tracks[track_uri]),
                    points=0,
                    cap_points=0,
                    is_submitter=False,
                )
                missing_votes.append(blank_vote)

    return missing_votes


def flatten_data(
    all_files: csv_model.AllFiles, tracks: dict[str, spotify.Track]
) -> list[FlatVote]:
    """Flattens and concatentates all CSV votes and submissions into one list."""
    flat_votes = []

    competitors = {c.ID: c.Name for c in all_files.competitors}
    rounds = {r.ID: r.Name for r in all_files.rounds}

    # Number of points to implicitly assign to one's own submission
    self_submission_points = len(competitors)

    for submission in all_files.submissions:
        track = tracks[submission.SpotifyURI]
        flat_votes.append(
            FlatVote(
                round_id=submission.RoundID,
                round_name=rounds[submission.RoundID],
                voter_id=submission.SubmitterID,
                voter_name=competitors[submission.SubmitterID],
                **get_track_dict(track),
                points=self_submission_points,
                cap_points=VOTE_CAP_POINTS,
                is_submitter=True,
            )
        )

    for vote in all_files.votes:
        track = tracks[vote.SpotifyURI]
        flat_votes.append(
            FlatVote(
                round_id=vote.RoundID,
                round_name=rounds[vote.RoundID],
                voter_id=vote.VoterID,
                voter_name=competitors[vote.VoterID],
                **get_track_dict(track),
                points=vote.PointsAssigned,
                cap_points=min(vote.PointsAssigned, VOTE_CAP_POINTS),
                is_submitter=False,
            )
        )

    missing_votes = get_missing_votes(flat_votes, competitors, rounds, tracks)

    return flat_votes + missing_votes


def load_data(directory: str) -> list[FlatVote]:
    """Loads all the CSV in a given directory and returns a list of FlatVotes"""
    all_files = csv_model.load_csvs(directory)

    submissions = all_files.submissions
    track_uris = [s.SpotifyURI for s in submissions]
    tracks = spotify.get_tracks(track_uris)

    all_artist_ids = set()
    for track in tracks.values():
        for artist in track.artists:
            all_artist_ids.add(artist.id)

    flat_votes = flatten_data(all_files, tracks)
    return flat_votes


def write_flat_data(flat_votes: list[FlatVote], filename: str):
    """Writes a list of FlatVote items out to a given csv file"""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = FlatVote.model_fields
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in flat_votes:
            writer.writerow(row.model_dump())
