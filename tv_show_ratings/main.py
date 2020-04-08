import argparse
from datetime import datetime
import json
import re
import sys

from imdb import IMDb, IMDbError
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from tv_show_ratings import __version__, __title__


def get_args(sys_args):
    """parses the arguments from command line and returns them"""
    parser = argparse.ArgumentParser(
        description='Command line tool that creates rating charts '
        'for all episodes of a TV shows with data from IMDB',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'movie_ids',
        nargs='+',
        help='IMDB IDs of the series, e.g. part of the URL'
    )
    parser.add_argument(
        '-f', '--format',
        default='png',
        choices=[
            'eps', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz'
        ],
        help='format of the output document'
    )
    parser.add_argument(
        '--width',
        type=float,
        default=11.7,
        help='width of output document in inches'
    )
    parser.add_argument(
        '--height',
        type=float,
        default=8.27,
        help='height of output document in inches'
    )
    parser.add_argument(
        '--average-rating',
        type=float,
        default=6.39,
        help='"average" rating defines position of yellow color'
    )
    parser.add_argument(
        '--save-to-file',
        action='store_true',
        help='when set will save the data retrieved from IMDB to file'
    )
    parser.add_argument(
        '--load-from-file',        
        action='store_true',
        help='will load data from file instead of from IMDB'
    )
    return parser.parse_args(sys_args)


def generate_filename_series(movie_id):
    return f'tv_show_ratings_{movie_id}.json'


def generate_filename_chart(series, args):
    """returns the generated basename for files for this series"""
    s = str(series.get("title")).strip().replace(' ', '_')
    title_slug = re.sub(r'(?u)[^-\w.]', '', s)
    return f'tv_show_ratings_{series["movie_id"]}_{title_slug}.{args.format}'


def fetch_data_from_imdb(movie_id) -> dict:
    """Tries to fetch data for all episodes for given movie ID 
    and return them as dict

    Will return None if an error occurred
    """
    print(f'Trying to load series with ID {movie_id} from IMDB...')
    ia = IMDb()
    success = True
    try:
        series_obj = ia.get_movie(movie_id)
    except IMDbError as e:
        print(f'Failed to load series. Error was: {e}')
        success = False

    if success and series_obj.get('kind') != 'tv series':
        print(
            f'Sorry, but "{series_obj.get("title")}" is not a series. '
            f'Please double-check your ID.'
        )
        success = False

    if success:
        print(
            f'Loading episodes of \'{series_obj.get("title")}\' for '
            f'{series_obj.get("number of seasons")} seasons from IMDB...'
        )
        ia.update(series_obj, 'episodes')
        return convert_series_obj_to_dict(series_obj)
        
    else:
        return None


def convert_series_obj_to_dict(series_obj: object) -> dict:
    episodes_dct = dict()
    for season_no, episodes in series_obj['episodes'].items():
        if season_no not in episodes_dct:
            episodes_dct[season_no] = dict()
        for ep_no, episode in episodes.items():
            episodes_dct[season_no][ep_no] = {
                'rating': episode.get('rating'),
                'votes': episode.get('votes')
            }
    return {
        'movie_id': series_obj.getID(),
        'title': series_obj.get('title'),
        'kind': series_obj.get('kind'),
        'series years': series_obj.get('series years'),
        'episodes': episodes_dct
    }


def load_series_from_file(movie_id) -> dict:
    filename = generate_filename_series(movie_id)
    print(f'Loading series from file: {filename}')
    try:
        with open(filename, mode='r', encoding='utf8') as f:
            series = json.load(f)
    except Exception as ex:
        print(f'Failed to load {filename}: {ex}')
        series = None
    
    return series


def save_series_to_file(series) -> None:
    filename = generate_filename_series(series['movie_id'])
    print(f'Saving series to file: {filename}')
    try:
        with open(filename, mode='w', encoding='utf8') as f:
            json.dump(series, f)
    except Exception as ex:
        print(f'Failed to save {filename}: {ex}')


def convert_imdb_data_to_df(series: dict) -> pd.DataFrame:
    """converts raw data from IMDB into a pandas data frame and returns it
    
    optionally saves data frame
    """
    print(f'Creating plot for \'{series["title"]}\'...')
    raw_data = list()
    for season_no, episodes in series['episodes'].items():
        for ep_no, episode in episodes.items():
            raw_data.append({            
                'season': season_no,
                'episode': ep_no,
                'rating': episode.get('rating'),
                'votes': episode.get('votes')
            })

    df = pd.DataFrame(raw_data)
    df['season'] = pd.to_numeric(df['season'])
    df['episode'] = pd.to_numeric(df['episode'])
    return df
    

def get_pivot_data(df):
    ratings = pd.pivot_table(
        df, values='rating', index='episode', columns='season'
    )
    avg_votes = df["votes"].mean()
    return ratings, avg_votes


def generate_chart(series, ratings, avg_votes, args):
    """generates the chart for the give data and returns it as figure"""
    
    fig, ax = plt.subplots()
    fig.set_size_inches(args.width, args.height)    
    cmap = sns.blend_palette(('red', 'yellow', 'green'), as_cmap=True)
    sns.heatmap(
        ratings,     
        ax=ax,
        center=args.average_rating, 
        vmax=10,
        vmin=1,
        annot=True, 
        linewidths=.75, 
        cmap=cmap,
        fmt='.1f',
        xticklabels=True,
        yticklabels=True,
        cbar_kws={
            'label': f'IMDB rating (centered on {args.average_rating:,.2f})'
        }
    )
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.tick_params(left=False, top=False)
    ax.tick_params(axis='y', labelrotation=0)
    ax.set_title('IMDB rating for each episode')
    
    fig.subplots_adjust(top=.85)
    years = series['series years']
    fig.suptitle(f'{series["title"]} ({years})', fontsize='xx-large', va='top')
    today = datetime.utcnow().strftime('%Y-%m-%d')
    bottom_text = (
        f'Created on {today} with data from IMDB.com - '
        f'Average votes p. episode = {avg_votes:,.0f}'
    )
    plt.figtext(0.05, 0.05, bottom_text, fontsize='small')
    return fig


def save_chart(series, fig, args):
    """Saves the generated chart as file in the chosen format"""    
    filename = generate_filename_chart(series, args)
    print(f'Storing plot as {filename}')
    fig.savefig(filename)


def main():
    print(f'{__title__} v{__version__}')
    args = get_args(sys.argv[1:])
    if len(args.movie_ids) > 1:
        print(
            f'Will try to create charts for movie IDs:'
            f' {", ".join(args.movie_ids)}'
        )
    for movie_id in args.movie_ids:        
        if args.load_from_file:
            series = load_series_from_file(movie_id)
        else:
            series = fetch_data_from_imdb(movie_id)
            if series:
                if args.save_to_file:
                    save_series_to_file(series)

        if series:            
            ratings, avg_votes = get_pivot_data(convert_imdb_data_to_df(series))
            fig = generate_chart(series, ratings, avg_votes, args)
            save_chart(series, fig, args)            
            plt.close()


if __name__ == '__main__':
    main()
