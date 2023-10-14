"""Loads the CSV files into a list of pydantic models"""

import csv
import pathlib
from pydantic import BaseModel

from src import models


def load_csv(filename: pathlib.Path) -> list[BaseModel]:
    """Loads a given CSV filename into a corresponding list of objects"""
    lines = []
    model_class = models.FILE_TO_MODEL_MAP[filename.name]
    with open(filename, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        assert reader.fieldnames is not None
        reader.fieldnames = [x.replace(" ", "") for x in reader.fieldnames]
        for row in reader:
            lines.append(model_class(**row))
    return lines


def load_csvs(directory: str) -> dict[str, list[BaseModel]]:
    """Loads all the MusicLeague CSVs in a given directory"""
    all_models = {}
    for basename in models.FILE_TO_MODEL_MAP:
        filename = pathlib.Path(directory, basename)
        all_models[basename.replace(".csv", "")] = load_csv(filename)
    return all_models
