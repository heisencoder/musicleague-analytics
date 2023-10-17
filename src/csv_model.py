"""Loads the MusicLeague CSV files into pydantic models.

Pydantic models generated via datamodel-code-generator from actual JSON responses"""

import csv
import pathlib
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

    SpotifyURI: str  # Spotify Track URI
    SubmitterID: str  # Foreign key to Competitor.ID
    Created: str
    Comment: str
    RoundID: str  # Foreign key to Round.ID
    VisibleToVoters: str


class Vote(BaseModel):
    """A vote by a given competitor for a particular song in a given round"""

    SpotifyURI: str  # Spotify Track URI
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


def load_csv(filename: pathlib.Path) -> list[BaseModel]:
    """Loads a given CSV filename into a corresponding list of objects"""
    lines = []
    model_class = FILE_TO_MODEL_MAP[filename.name]
    with open(filename, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        assert reader.fieldnames is not None
        # remove spaces from headers to make it compatible with the pydantic classes.
        reader.fieldnames = [x.replace(" ", "") for x in reader.fieldnames]
        for row in reader:
            lines.append(model_class(**row))
    return lines


def load_csvs(directory: str) -> AllFiles:
    """Loads all the MusicLeague CSVs in a given directory"""
    all_models = {}
    for basename in FILE_TO_MODEL_MAP:
        filename = pathlib.Path(directory, basename)
        all_models[basename.replace(".csv", "")] = load_csv(filename)
    return AllFiles.model_validate(all_models)
