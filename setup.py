import os 
from setuptools import find_packages, setup

from tv_show_ratings import __version__

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='tv-show-ratings',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description=(
        'Command line tool that creates a ratings chart for all episodes of '
        'a TV show based on IMDB'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['imdb', 'heatmap'],
    url='https://github.com/ErikKalkoken/tv-show-ratings',
    author='Erik Kalkoken',
    author_email='kalkoken87@gmail.com',
    classifiers=[        
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',                
        'Programming Language :: Python :: 3.7',   
    ],
    python_requires='>=3.6',    
    install_requires=[
        'seaborn',
        'imdbpy'
    ],    
    entry_points={
        'console_scripts': [
            'tv_show_ratings=tv_show_ratings.main:main',
        ],
    },
)
