"""Interface to spotify API to download track information

These Pydantic BaseModel classes were generated via a JSON download from Spotify, followed by a
conversion from JSON to Pydantic via https://jsontopydantic.com/
"""

from typing import Any, List, Optional

from pydantic import BaseModel

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# See this limit here:
# https://developer.spotify.com/documentation/web-api/reference/get-several-tracks
MAX_TRACKS_PER_CALL = 50


class ExternalUrls(BaseModel):
    """Known external URLs for this track."""

    spotify: str


class Artist(BaseModel):
    """The artists who performed the track.
    Each artist object includes a link in href to more detailed information about the artist.
    """

    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class Image(BaseModel):
    """The cover art for the album in various sizes, widest first."""

    height: int
    url: str
    width: int


class Album(BaseModel):
    """The album on which the track appears.
    The album object includes a link in href to full information about the album."""

    album_type: str
    artists: List[Artist]
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


def get_tracks(tids: list[str]) -> dict[str, Track]:
    """Returns Spotify track details for a given list of Spotify URI tracks"""

    # Based on https://github.com/spotipy-dev/spotipy/blob/master/examples/show_tracks.py
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    tracks = {}

    for start in range(0, len(tids), MAX_TRACKS_PER_CALL):
        results = sp.tracks(tids[start : start + MAX_TRACKS_PER_CALL])
        for track in results["tracks"]:
            track_obj = Track.model_validate(track)
            tracks[track_obj.uri] = track_obj

    return tracks
