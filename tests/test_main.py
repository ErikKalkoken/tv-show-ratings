from argparse import Namespace
from unittest import TestCase
from unittest.mock import Mock, patch

from imdb import IMDbError
import pandas as pd

from .no_sockets import NoSocketsTestCase
from .testdata import test_series, test_series_obj, test_raw_data
from tv_show_ratings.main import (
    get_args, 
    generate_filename_chart,
    generate_filename_series,
    fetch_data_from_imdb,
    convert_imdb_data_to_df,
    convert_series_obj_to_dict
)


MODULE_PATCH = 'tv_show_ratings.main'


class TestGetArgs(TestCase):

    def test_get_movie_id(self):
        expected = Namespace(
            movie_ids=['01234'],
            format='png', 
            width=11.7, 
            height=8.27, 
            load_from_file=False,
            average_rating=6.39,
            save_to_file=False,            
        )
        self.assertEqual(get_args(['01234']), expected)


@patch(MODULE_PATCH + '.IMDb')
class TestFetchDataFromImdb(NoSocketsTestCase):
    
    @staticmethod
    def mock_series_get(param):
        if param == 'title':
            return 'My Title'
        elif param == 'kind':
            return 'tv series'

    @staticmethod
    def mock_series_get_no_series(param):
        if param == 'title':
            return 'My Title'
        elif param == 'kind':
            return 'movie'
    
    def test_returns_series_normally(self, mock_imdb):
        mock_series = Mock()
        mock_series.get.side_effect = self.mock_series_get
        mock_imdb.return_value.get_movie.return_value = test_series_obj
                
        expected = test_series
        self.assertEqual(fetch_data_from_imdb('01234'), expected)

    def test_returns_none_on_exception(self, mock_imdb):
        mock_series = Mock()
        mock_series.get.side_effect = self.mock_series_get
        mock_imdb.return_value.get_movie.side_effect = IMDbError
        
        expected = None
        self.assertEqual(fetch_data_from_imdb('01234'), expected)

    def test_returns_none_for_non_series(self, mock_imdb):
        mock_series = Mock()
        mock_series.get.side_effect = self.mock_series_get_no_series
        mock_imdb.return_value.get_movie.return_value = mock_series
        
        expected = None
        self.assertEqual(fetch_data_from_imdb('01234'), expected)


class TestConvertImdbDataToDf(TestCase):

    def test_convert_imdb_data_to_df(self):        
        expected_df = pd.DataFrame(test_raw_data)
        my_df = convert_imdb_data_to_df(test_series)
        pd.testing.assert_frame_equal(my_df, expected_df)


class TestMain(NoSocketsTestCase):
    
    def test_generate_filename_chart(self):        
        expected = 'tv_show_ratings_01234_My_Title.png'
        self.assertEqual(
            generate_filename_chart(test_series, Namespace(format='png')), 
            expected
        )

    def test_generate_filename_series(self):
        movie_id = '01234'
        expected = 'tv_show_ratings_01234.json'
        self.assertEqual(generate_filename_series(movie_id), expected)

    def test_convert_series_obj_to_dict(self):
        self.assertDictEqual(
            convert_series_obj_to_dict(test_series_obj),
            test_series
        )
