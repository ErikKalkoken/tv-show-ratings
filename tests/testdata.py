class MyEpisode:

    def __init__(self, rating: float, votes: int) -> None:
        self._rating = float(rating)
        self._votes = int(votes)
        
    def get(self, param: str):
        if param == 'rating':
            return self._rating
        elif param == 'votes':
            return self._votes
        else:
            raise ValueError(f'Invalid param {param}')


class MySeries(dict):

    def __init__(
        self, 
        movie_id: str, 
        title: str, 
        kind: str,
        years: str,
        episodes: dict = None
    ):
        self._movie_id = str(movie_id)
        self._title = str(title)
        self._kind = str(kind)
        self._years = str(years)
        self['episodes'] = episodes

    def __getattr__(self, key):
        return self[key]

    def get(self, param: str):
        if param == 'title':
            return self._title        
        elif param == 'kind':
            return self._kind
        elif param == 'series years':
            return self._years      
        elif param == 'number of seasons':
            return len(self['episodes'].keys())
        else:
            raise ValueError(f'Invalid param {param}')

    def getID(self) -> str:
        return self._movie_id


test_series_obj = MySeries(
    '01234',
    'My Title',
    'tv series',
    '2001 - 2006',
    {    
        2: {
            1: MyEpisode(8.0, 100),
            2: MyEpisode(7.5, 200),
            3: MyEpisode(6.5, 300),
        },
        1: {
            1: MyEpisode(8.5, 200),
            2: MyEpisode(9.0, 300),
        },
    }
)

test_series = {
    'movie_id': '01234',
    'title': 'My Title',
    'kind': 'tv series',
    'series years': '2001 - 2006',
    'episodes': {
        2: {
            1: {
                'rating': 8.0,
                'votes': 100
            },
            2: {
                'rating': 7.5,
                'votes': 200
            },            
            3: {
                'rating': 6.5,
                'votes': 300
            }
        },
        1: {
            1: {
                'rating': 8.5,
                'votes': 200
            },
            2: {
                'rating': 9.0,
                'votes': 300
            }
        },
    }
}

test_raw_data = [   
    {
        'season': 2,
        'episode': 1,
        'rating': 8.0,
        'votes': 100
    },
    {
        'season': 2,
        'episode': 2,
        'rating': 7.5,
        'votes': 200
    },            
    {
        'season': 2,
        'episode': 3,
        'rating': 6.5,
        'votes': 300
    },            
    {
        'season': 1,
        'episode': 1,
        'rating': 8.5,
        'votes': 200
    },           
    {
        'season': 1,
        'episode': 2,
        'rating': 9.0,
        'votes': 300
    },            
]
