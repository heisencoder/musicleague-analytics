# Pydantic models for JSON responses from Music League Server
# Generated via datamodel-code-generator from actual JSON responses

from typing import List

from pydantic import BaseModel


class Round(BaseModel):
    id: str
    name: str
    completed: str
    description: str
    downvotesPerUser: int
    highStakes: bool
    leagueId: str
    maxDownvotesPerSong: int
    maxUpvotesPerSong: int
    playlistUrl: str
    sequence: int
    songsPerUser: int
    startDate: str
    status: str
    submissionsDue: str
    upvotesPerUser: int
    votesDue: str
    templateId: str


class Rounds(BaseModel):
    __root__: List[Round]


class Submission(BaseModel):
    created: str
    submitterId: str
    spotifyUri: str
    comment: str
    commentVisibility: str


class Vote(BaseModel):
    comment: str
    created: str
    spotifyUri: str
    voterId: str
    weight: int


class Standing(BaseModel):
    pointsActual: int
    pointsPossible: int
    rank: int
    submission: Submission
    submitterVoted: bool
    tieBreaker: str
    votes: List[Vote]


class Standings(BaseModel):
    standings: List[Standing]


class User(BaseModel):
    id: str
    name: str
    profileImage: str


class Member(BaseModel):
    chatReadMarker: str
    created: str
    isAdmin: bool
    isPlayer: bool
    mine: bool
    user: User


class Members(BaseModel):
    __root__: List[Member]
