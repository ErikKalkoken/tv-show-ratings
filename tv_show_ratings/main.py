import argparse
import re

import numpy as np
import seaborn as sns
import pandas as pd
from imdb import IMDb, IMDbError

from . import __version__

def get_args():
    """parses the arguments from command line and returns them"""
    parser = argparse.ArgumentParser(
        description='Creates a ratings chart for all episodes of a TV show '
        'based on current IMDB ratings'
    )
    parser.add_argument(
        'movie_ids', 
        nargs='+', 
        help='IMDB IDs of the series, e.g. part of the URL'
    )
    parser.add_argument(
        '-f', '--format',
        default='png',
        choices=['eps', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz'],
        help='Format of the output document. Default is \'png\''
    )
    parser.add_argument(
        '--width',
        type=float,
        default=11.7,
        help='Width of output document in inches'
    )
    parser.add_argument(
        '--height',
        type=float,
        default=8.27,
        help='Height of output document in inches'
    )
    parser.add_argument(
        '--rating-center',
        type=float,
        default=6.39,
        help='rating for "average" rating = yellow. Default is 6.39'
    )
    return parser.parse_args()

def fetch_data_from_IMDB(movie_id):
    """Tries to fetch data for all episodes for given movie ID and return them
    
    Will return False if an error occurred
    """
    print(f'Trying to load series with ID {movie_id} from IMDB...')
    ia = IMDb()    
    success = True
    try:
        series = ia.get_movie(movie_id)        
    except IMDbError as e:
        print(f'Failed to load series. Error was: {e}')
        success = False
    
    if series.get('kind') != 'tv series':
        print(
            f'Sorry, but "{series.get("title")}" is not a series. '
            f'Please double-check your ID.'
        )
        success = False

    if success:
        print(
            f'Loading episodes of \'{series.get("title")}\' for '
            f'{series.get("number of seasons")} seasons from IMDB...'
        )
        ia.update(series, 'episodes')
        return series
    else:
        return None

def convert_imdb_data_to_pivot(series):
    """converts raw data from IMDB into a pandas pivot with ratings and returns it"""
    print(f'Creating plot for \'{series.get("title")}\'...')
    raw_data = list()
    for season_no, episodes in series['episodes'].items():
        for ep_no, episode in episodes.items():
            raw_data.append({            
                'season': season_no,
                'episode': ep_no,
                'rating': episode.get('rating')
            })

    df = pd.DataFrame(raw_data)
    return pd.pivot_table(df, values='rating', index='episode', columns='season')

def generate_chart(series, ratings, args):
    """generates the heatmap chart for the give data and returns it as figure"""
    sns.set(rc={'figure.figsize': (args.width, args.height)})
    cmap = sns.blend_palette(('red', 'yellow', 'green'), as_cmap=True)
    ax = sns.heatmap(
        ratings,     
        center=args.rating_center, 
        vmax=10,
        vmin=1,
        annot=True, 
        linewidths=.75, 
        cmap=cmap,
        fmt='.1f',
        xticklabels=True,
        yticklabels=True,
        cbar_kws={'label': 'IMDB rating'}
    )
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.tick_params(left=False, top=False)
    ax.tick_params(axis='y', labelrotation=0)    
    fig = ax.get_figure()
    fig.subplots_adjust(top=.87)
    years = series.get('series years')
    fig.suptitle(f'{series.get("title")} ({years})', fontsize=16, va='top')    
    return fig

def save_chart(series, fig, movie_id, args):
    """Saves the generated chart as file in the chosen format"""
    s = str(series.get("title")).strip().replace(' ', '_')
    title_slug = re.sub(r'(?u)[^-\w.]', '', s)
    filename = f'tv_show_ratings_{movie_id}_{title_slug}.{args.format}'
    print(f'Storing plot as {filename}')
    fig.savefig(filename)

def main():
    print(f'TV series ratings v{__version__}')
    args = get_args()
    if len(args.movie_ids)> 0:
        print(
            f'Will try to create charts for movie IDs:'
            f' {", ".join(args.movie_ids)}'
        )
    for movie_id in args.movie_ids:
        series = fetch_data_from_IMDB(movie_id)
        if series:
            ratings = convert_imdb_data_to_pivot(series)    
            fig = generate_chart(series, ratings, args)    
            save_chart(series, fig, movie_id, args)
            fig.clf()   # clear figure for next iteration

if __name__ == '__main__':
    main()