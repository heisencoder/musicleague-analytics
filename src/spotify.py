"""Interface to spotify API to download track information

These Pydantic BaseModel classes were generated via a JSON download from Spotify, followed by a
conversion from JSON to Pydantic via https://jsontopydantic.com/
"""

from functools import cache
from typing import Any, Callable, List, Optional

from pydantic import BaseModel

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# See this limit here:
# https://developer.spotify.com/documentation/web-api/reference/get-several-tracks
MAX_TRACKS_PER_CALL = 50


class ExternalUrls(BaseModel):
    """Known external URLs for this track."""

    spotify: str


class SimplifiedArtist(BaseModel):
    """A simplified Spotify artist who performed the track or album."""

    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class Followers(BaseModel):
    """Information about the followers of the artist."""

    href: Optional[str]
    total: int


class Image(BaseModel):
    """The cover art for the album in various sizes, widest first."""

    height: int
    url: str
    width: int


class Artist(BaseModel):
    """A spotify Artist"""

    external_urls: ExternalUrls
    followers: Optional[Followers] = None
    genres: Optional[List[str]] = None
    href: str
    id: str
    images: Optional[List[Image]] = None
    name: str
    popularity: Optional[int] = None
    type: str
    uri: str


class Album(BaseModel):
    """The album on which the track appears.
    The album object includes a link in href to full information about the album."""

    album_type: str
    artists: List[SimplifiedArtist]
    available_markets: List[str]
    external_urls: ExternalUrls
    href: str
    id: str
    images: List[Image]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


class ExternalIds(BaseModel):
    """Known external IDs for the track."""

    isrc: Optional[str] = None
    ean: Optional[str] = None
    upc: Optional[str] = None


class Track(BaseModel):
    """See https://developer.spotify.com/documentation/web-api/reference/get-several-tracks"""

    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIds
    external_urls: ExternalUrls
    href: str
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: Optional[Any] = None
    track_number: int
    type: str
    uri: str


@cache
def get_spotipy_client() -> spotipy.Spotify:
    """Returns a new spotipy client using tokens stored via environment variables"""
    client_credentials_manager = SpotifyClientCredentials()
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def _chunk_calls(func: Callable, result_key: str, ids: list[str]) -> Any:
    """Generator that yields items from a batch API call.

    Params:
        func - The function to call with a list of string IDs in small batches
        result_key - The key of the resulting dict that contains a list of items
        ids - A list of IDs to pass to the callable func

    Yields:
        a stream of results from this particular API call
    """
    for start in range(0, len(ids), MAX_TRACKS_PER_CALL):
        results = func(ids[start : start + MAX_TRACKS_PER_CALL])
        for result in results[result_key]:
            yield result


def get_tracks(tids: list[str]) -> dict[str, Track]:
    """Returns Spotify track details for a given list of Spotify URI tracks

    Returns a dictionary of Spotify URI to the corresponding Track object.
    """

    # Based on https://github.com/spotipy-dev/spotipy/blob/master/examples/show_tracks.py
    sp = get_spotipy_client()

    tracks = {}

    for track in _chunk_calls(sp.tracks, "tracks", tids):
        track_obj = Track.model_validate(track)
        tracks[track_obj.uri] = track_obj

    # Note that despite documenting a Track as containing the full Artist,
    # it actually contains a SimplifiedArtis. The remain code augments each
    # track with a full Artist list, including fields like genre.

    # Make a set of all unique artist IDs that appear in all the tracks
    all_artist_ids = set()
    for track in tracks.values():
        for artist in track.artists:
            all_artist_ids.add(artist.id)

    # Get the detailed artist information for all the artists in the tracks
    artists = get_artists(list(all_artist_ids))

    # Replace the SimplifiedArtist instances with the full Artist for each track
    for track in tracks.values():
        artist_ids = track.artists
        track.artists = [artists[a.id] for a in artist_ids]

    return tracks


def get_artists(artist_ids: list[str]) -> dict[str, Artist]:
    """Returns a dict of Spotify Artist objects from a given list of Artist IDs"""
    sp = get_spotipy_client()

    artists = {}

    for artist in _chunk_calls(sp.artists, "artists", artist_ids):
        artist_obj = Artist.model_validate(artist)
        artists[artist_obj.id] = artist_obj

    return artists
