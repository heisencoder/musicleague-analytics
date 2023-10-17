# musicleague-analytics

Analytics Tools for Music League

## Overview

This repository contains some simple tools for helping to analyze the CSV files from a given
[MusicLeague](https://app.musicleague.com/) league.

This requires a league CSV download, which you can do via becoming a
[Patreon member for MusicLeague](https://www.patreon.com/musicleague/posts), which should enable
this download.

This repo is very much in draft form right now, and assumes that you are comfortable using Python
and the command-line in a terminal.

## Installing Python packages

This project uses Python3 and [Poetry](https://python-poetry.org/) as the package manager.
You need to install poetry and use it to install the needed Python packages.

## Getting a Spotify access token

This package requires access to the (Spotify API)[https://developer.spotify.com/documentation/web-api)
for downloading song details from the MusicLeague CSV files.  In particular, you will need to
follow the Spotify API instructions for creating these.  Once you do that, you need to populate
the following environment variables, which are used by the spotipy Python package:

```shell
export SPOTIPY_CLIENT_ID=<your_client_id>
export SPOTIPY_CLIENT_SECRET=<your_client_secret>
```

## Downloading data

You will need to download the CSV data for a given MusicLeague league.  If you are a patreon
subscriber for MusicLeague, then on the league's homepage, this should enable a pull-down under
the "Action" menu labeled "Export League Data".  This will download a zip file that you will need
to extract into a new directory named `data` in your local copy of this repository.

## Running the analyzer

In a terminal, run

```shell
poetry run python3 src/analyze.py --directory data --output_file flat_data.csv
```
