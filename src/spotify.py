"""Interface to spotify API to download track information"""

from typing import Any, List, Optional

from pydantic import BaseModel

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


MAX_TRACKS_PER_CALL = 50


class ExternalUrls(BaseModel):
    spotify: str


class Artist(BaseModel):
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str


class Image(BaseModel):
    height: int
    url: str
    width: int


class Album(BaseModel):
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
    isrc: str


class Track(BaseModel):
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
    preview_url: Any
    track_number: int
    type: str
    uri: str


def get_tracks(tids: list[str]) -> list[dict]:
    """Returns Spotify track details for a given list of Spotify URI tracks"""
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    tracks = []

    for start in range(0, len(tids), MAX_TRACKS_PER_CALL):
        results = sp.tracks(tids[start : start + MAX_TRACKS_PER_CALL])
        for track in results["tracks"]:
            tracks.append(Track.model_validate(track))

    return tracks
