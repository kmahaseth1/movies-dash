import sqlite3
import pandas as pd 
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from film_details import get_movie_details

# Update the current working directory to the main project folder
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# API call setup
load_dotenv()
api_key = os.getenv("TMDB_API")
details_url = "https://api.themoviedb.org/3/movie/"

# Read the CSV with ids
ids = pd.read_csv('data/id_list.csv')

# Connect to SQLite database
con = sqlite3.connect('movies_2020s.db')

# Create table if it does not exist
con.execute(
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
        genre TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    '''
)

# Fill the raw data table
for id in ids:
    try:
        # Ensure the data for the id does not already exist
        check = pd.read_sql(
            "SELECT tmdb_id FROM movie_data_raw WHERE id = ?",
            con,
            params=[id]
        )
        
        if len(check) > 0:
            continue

        # Get the data using an API call and append to the table
        film_dict = get_movie_details(details_url, api_key, id)
        film = pd.DataFrame(film_dict)

        film.to_sql('movie_data_raw', con, if_exists='append', index=False)
    
    except Exception as e:
        # Store error
        con.execute(
            '''
            INSERT INTO movie_data_raw (
                tmdb_id, name, budget, genres, production_countries, revenue,
                vote_average, release_year, type, genre
                ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (id, None, None, None, None, None, None, None, None, None)
        )
    
    # Brief sleep to respect rate limits
    time.sleep(0.5)

con.commit()
con.close()