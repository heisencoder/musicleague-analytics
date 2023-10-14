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

## Downloading data

You will need to download the CSV data for a given MusicLeague league.  If you are a patreon
subscriber for MusicLeague, then on the league's homepage, this should enable a pull-down under
the "Action" menu labeled "Export League Data".  This will download a zip file that you will need
to extract into a new directory named `data` in your local copy of this repository.

## Installing Python packages

This project uses Python3 and [Poetry](https://python-poetry.org/) as the package manager.
You need to install poetry and use it to install the needed Python packages.

## Running the analyzer

In a terminal, run

```shell
poetry run python3 src/analyze.py --directory data
```
