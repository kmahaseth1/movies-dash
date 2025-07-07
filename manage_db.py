import sqlite3
import pandas as pd 
import requests
import time
import os
from datetime import datetime
from film_details import get_movie_details

# Update the current working directory to the main project folder
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Read the CSV with ids
ids_df = pd.read_csv('data/id_list.csv')

# Connect to SQLite database
connection = sqlite3.connect('movies_2020s.db')

# Create table if it does not exist
connection.execute(
    '''
    CREATE TABLE IF NOT EXISTS movie_data_raw (
        tmdb_id INTEGER PRIMARY KEY,
        name TEXT,
        budget INTEGER,
        genres TEXT,
        production_countries TEXT,
        revenue INTEGER,
        vote_average REAL,
        release_year TEXT,
        type TEXT,
        genre TEXT
    )
    '''
)

connection.close()