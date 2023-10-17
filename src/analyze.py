"""Main entry point for musicleague-analysis package.

This module will parse arguments and perform commands
"""

import argparse

from src import flat_model

parser = argparse.ArgumentParser()
parser.add_argument(
    "--directory",
    dest="directory",
    help="Directory containing MusicLeague CSV files",
    type=str,
    default="data",
)
parser.add_argument(
    "--output_file",
    dest="output_file",
    help="filename to write flattened data out to",
    type=str,
    default="flat_data.csv",
)


def main(args: argparse.Namespace):
    """Main entry point for MusicLeague analyzer"""
    directory = args.directory
    flat_votes = flat_model.load_data(directory)
    flat_model.write_flat_data(flat_votes, args.output_file)


if __name__ == "__main__":
    _args = parser.parse_args()
    main(_args)
