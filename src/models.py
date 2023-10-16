"""Pydantic models for JSON responses from Music League Server
Generated via datamodel-code-generator from actual JSON responses"""

from pydantic import BaseModel


class Competitor(BaseModel):
    """A single user in a given MusicLeague"""

    ID: str
    Name: str


class Round(BaseModel):
    """A MusicLeague round"""

    ID: str
    Created: str
    Name: str
    Description: str
    PlaylistURL: str


class Submission(BaseModel):
    """A song submission by a competitor for a particular round"""

    SpotifyURI: str
    SubmitterID: str  # Foreign key to Competitor.ID
    Created: str
    Comment: str
    RoundID: str  # Foreign key to Round.ID
    VisibleToVoters: str


class Vote(BaseModel):
    """A vote by a given competitor for a particular song in a given round"""

    SpotifyURI: str
    VoterID: str  # Foreign key to Competitor.ID
    Created: str
    PointsAssigned: str
    Comment: str
    RoundID: str  # Foreign key to Round.ID


FILE_TO_MODEL_MAP = {
    "competitors.csv": Competitor,
    "rounds.csv": Round,
    "submissions.csv": Submission,
    "votes.csv": Vote,
}


class AllFiles(BaseModel):
    """All the data from all the CSV files in a given MusicLeague Export"""

    competitors: list[Competitor]
    rounds: list[Round]
    submissions: list[Submission]
    votes: list[Vote]
