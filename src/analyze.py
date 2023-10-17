"""Main entry point for musicleague-analysis package.

This module will parse arguments and perform commands
"""

import argparse
from collections import defaultdict
from pprint import pprint

from pydantic import BaseModel

from src import csv_model

# from src import spotify

parser = argparse.ArgumentParser()
parser.add_argument(
    "--directory",
    dest="directory",
    help="Directory containing MusicLeague CSV files",
    type=str,
    default="data",
)


class FlatVote(BaseModel):
    """A flattened version of a Vote or Submission"""

    round_id: str  # Round.ID
    round_name: str  # Foreign key to Round.Name
    voter_id: str  # Competitor.ID
    voter_name: str  # Foreign key to Competitor.Name
    track_uri: str  # Spotify Track URI
    track_name: str
    track_artist: str
    points: int  # Number of points given to song by voter. Self-submissions included
    is_submitter: bool  # Whether this person submitted the song


def get_missing_votes(
    votes: list[FlatVote], competitors: dict[str, str], rounds: dict[str, str]
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
        round_voters[vote.round_id].add(vote.voter_id)
        round_songs[vote.round_id].add(vote.track_uri)
        round_song_voters[vote.round_id][vote.track_uri].add(vote.voter_id)

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
                    track_uri=track_uri,
                    track_name="",
                    track_artist="",
                    points=0,
                    is_submitter=False,
                )
                pprint(blank_vote)
                missing_votes.append(blank_vote)

    return missing_votes


def flatten_data(all_files: csv_model.AllFiles) -> list[FlatVote]:
    """Flattens and concatentates all CSV votes and submissions into one list."""
    flat_votes = []

    competitors = {c.ID: c.Name for c in all_files.competitors}
    rounds = {r.ID: r.Name for r in all_files.rounds}

    # Number of points to implicitly assign to one's own submission
    self_submission_points = len(competitors)

    for submission in all_files.submissions:
        flat_votes.append(
            FlatVote(
                round_id=submission.RoundID,
                round_name=rounds[submission.RoundID],
                voter_id=submission.SubmitterID,
                voter_name=competitors[submission.SubmitterID],
                track_uri=submission.SpotifyURI,
                track_name="",
                track_artist="",
                points=self_submission_points,
                is_submitter=True,
            )
        )

    for vote in all_files.votes:
        flat_votes.append(
            FlatVote(
                round_id=vote.RoundID,
                round_name=rounds[vote.RoundID],
                voter_id=vote.VoterID,
                voter_name=competitors[vote.VoterID],
                track_uri=vote.SpotifyURI,
                track_name="",
                track_artist="",
                points=vote.PointsAssigned,
                is_submitter=False,
            )
        )

    missing_votes = get_missing_votes(flat_votes, competitors, rounds)

    return flat_votes + missing_votes


def load_data(directory: str) -> list[FlatVote]:
    """Loads all the CSV in a given directory and returns a list of FlatVotes"""
    all_files = csv_model.load_csvs(directory)
    print(
        f"len(votes)={len(all_files.votes)}, len(submissions)={len(all_files.submissions)}"
    )
    flat_votes = flatten_data(all_files)
    for vote in flat_votes:
        pprint(vote)
    print(f"len(votes)={len(flat_votes)}")
    return flat_votes
    # submissions = all_files.submissions
    # track_uris = [s.SpotifyURI for s in submissions]
    # tracks = spotify.get_tracks(track_uris)
    # pprint(tracks["spotify:track:0V3wPSX9ygBnCm8psDIegu"])


def main(args: argparse.Namespace):
    """Main entry point for MusicLeague analyzer"""
    directory = args.directory
    load_data(directory)


if __name__ == "__main__":
    _args = parser.parse_args()
    main(_args)
