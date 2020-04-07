# tv-show-ratings

![version](https://img.shields.io/badge/version-0.1.0-orange)
![python](https://img.shields.io/badge/python-3.7-blue)
![license](https://img.shields.io/github/license/ErikKalkoken/dhooks-lite)

## Overview

**tv-show-ratings** is command line tool that creates ratings charts for all episodes of a TV show based on IMDB.

Example output:

![Star Trek](https://i.imgur.com/QltebUR.png)

This tool is powered by [imdbpy](https://github.com/alberanid/imdbpy), [seaborn](https://github.com/mwaskom/seaborn) and [pandas](https://github.com/pandas-dev/pandas).

## Features

- Creates heatmap of all episode ratings for a TV show based on IMDB
- Uses fixed color scale to that TV shows can be compared
- Color scale is centered on the latests IMDB average rating, which is 6.39 ([Source](https://www.quora.com/What-is-an-average-rating-on-IMDB-for-a-movie))
- Uses current IMDB ratings

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

You can also provide multiple IDs to generate charts for multiple TV shows in bulk.

Here is an overview of all options:

```text
usage: tv_show_ratings [-h] [-f {eps,pdf,pgf,png,ps,raw,rgba,svg,svgz}]
                       [--width WIDTH] [--height HEIGHT]
                       [--rating-center RATING_CENTER]
                       movie_ids [movie_ids ...]

Creates a ratings chart for all episodes of a TV show based on current IMDB
ratings

positional arguments:
  movie_ids             IMDB IDs of the series, e.g. part of the URL

optional arguments:
  -h, --help            show this help message and exit
  -f {eps,pdf,pgf,png,ps,raw,rgba,svg,svgz}, --format {eps,pdf,pgf,png,ps,raw,rgba,svg,svgz}
                        Format of the output document. Default is 'png'
  --width WIDTH         Width of output document in inches
  --height HEIGHT       Height of output document in inches
  --rating-center RATING_CENTER
                        rating for "average" rating = yellow. Default is 6.39
```
