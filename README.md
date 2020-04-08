# tv-show-ratings

![version](https://img.shields.io/badge/version-0.2.0-orange)
![python](https://img.shields.io/badge/python-3.6|3.7|3.8-blue)
![license](https://img.shields.io/github/license/ErikKalkoken/dhooks-lite)

## Overview

**tv-show-ratings** is command line tool that creates rating charts for all episodes of a TV shows with data from IMDB.

Example output:

![Star Trek](https://i.imgur.com/mYF0lDy.png)

This tool is powered by [imdbpy](https://github.com/alberanid/imdbpy), [seaborn](https://github.com/mwaskom/seaborn) and [pandas](https://github.com/pandas-dev/pandas).

## Features

- Creates a rating chart for all episodes of a TV show with data from IMDB
- Uses a fixed color scale to that TV shows can be compared
- The color scale is defined around 3 colors: green for the highest possible rating, red for the lowest possible rating and yellow for the average rating as defined by IMDB's overall average rating ([Source](https://www.quora.com/What-is-an-average-rating-on-IMDB-for-a-movie))
- Charts will be created using IMDB's current live data

## Installation

You can install this tool directly from the repo on any machine that runs Python 3:

```bash
pip install git+https://github.com/ErikKalkoken/tv-show-ratings
```

## Usage

After installation the tool can be started from the command line. For example to create a rating chart for Star Trek - The Next Generation with has the IMDB ID of 0092455:

```bash
tv_show_ratings 0092455
```

Note that you can get the IMDB ID from the URL of the series on IMDB.

You can also provide multiple IDs to generate charts for multiple TV shows in bulk:

```bash
tv_show_ratings 0092455 2306299
```

Here is an overview of all options:

```text
TV Show Ratings v0.2.0
usage: tv_show_ratings [-h] [-f {eps,pdf,pgf,png,ps,raw,rgba,svg,svgz}]
                       [--width WIDTH] [--height HEIGHT]
                       [--average-rating AVERAGE_RATING] [--save-to-file]
                       [--load-from-file]
                       movie_ids [movie_ids ...]

Command line tool that creates rating charts for all episodes of a TV shows
with data from IMDB

positional arguments:
  movie_ids             IMDB IDs of the series, e.g. part of the URL

optional arguments:
  -h, --help            show this help message and exit
  -f {eps,pdf,pgf,png,ps,raw,rgba,svg,svgz}, --format {eps,pdf,pgf,png,ps,raw,rgba,svg,svgz}
                        format of the output document (default: png)
  --width WIDTH         width of output document in inches (default: 11.7)
  --height HEIGHT       height of output document in inches (default: 8.27)
  --average-rating AVERAGE_RATING
                        "average" rating defines position of yellow color
                        (default: 6.39)
  --save-to-file        when set will save the data retrieved from IMDB to
                        file (default: False)
  --load-from-file      will load data from file instead of from IMDB
                        (default: False)
```
