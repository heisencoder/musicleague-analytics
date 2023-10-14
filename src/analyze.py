"""Main entry point for musicleague-analysis package.

This module will parse arguments and perform commands
"""

import argparse
import pprint

from src import load_csv

parser = argparse.ArgumentParser()
parser.add_argument(
    "--directory",
    dest="directory",
    help="Directory containing MusicLeague CSV files",
    type=str,
)


def main(args: argparse.Namespace):
    """Main entry point for MusicLeague analyzer"""
    directory = args.directory
    all_files = load_csv.load_csvs(directory)
    pprint.pprint(all_files)


if __name__ == "__main__":
    _args = parser.parse_args()
    main(_args)
