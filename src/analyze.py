"""Main entry point for musicleague-analysis package.

This module will parse arguments and perform commands
"""

import argparse
import pprint

from src import load_csv
from src import spotify

parser = argparse.ArgumentParser()
parser.add_argument(
    "--directory",
    dest="directory",
    help="Directory containing MusicLeague CSV files",
    type=str,
    default="data",
)


def main(args: argparse.Namespace):
    """Main entry point for MusicLeague analyzer"""
    directory = args.directory
    all_files = load_csv.load_csvs(directory)
    submissions = all_files.submissions
    track_uris = [s.SpotifyURI for s in submissions]
    tracks = spotify.get_tracks(track_uris)
    pprint.pprint(tracks["spotify:track:0V3wPSX9ygBnCm8psDIegu"])


if __name__ == "__main__":
    _args = parser.parse_args()
    main(_args)
