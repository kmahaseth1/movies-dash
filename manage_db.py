import sqlite3
import pandas as pd 
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from film_details import get_movie_details

# Update the current working directory to the main project folder
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Batch Processing configuration
BATCH_SIZE = 100
COMMIT_FREQUENCY = 50

# API call setup
load_dotenv()
api_key = os.getenv("TMDB_API")
details_url = "https://api.themoviedb.org/3/movie/"

# Read the CSV with ids and convert it to a list
ids = pd.read_csv('data/id_list.csv', header=None)
ids = ids.values.flatten().tolist()
ids = set(ids)

# Connect to SQLite database
con = sqlite3.connect('movies_2020s.db')

# Create the raw table
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
        production_country TEXT
    )
    '''
)
# Check for already processed ids to prevent dupilcation
processed_ids = set()
current_ids = pd.read_sql("SELECT tmdb_id FROM movie_data_raw", con)
if len(current_ids) > 0:
    processed_ids = set(current_ids['tmdb_id'].tolist())

remaining_ids = [id for id in ids if id not in processed_ids]

# Fill the raw data table in batches
total_batches = (len(remaining_ids) + BATCH_SIZE - 1) // BATCH_SIZE
processed_count = 0

for batch in range(total_batches):
    start = batch * BATCH_SIZE
    end = min((batch+ 1) * BATCH_SIZE, len(remaining_ids))
    batch_ids = remaining_ids[start:end]

    print(f"\n--- Processing Batch {batch + 1}/{total_batches} ---")
    print(f"IDs {start+ 1} to {end} of {len(remaining_ids)}")

    batch_success = 0
    batch_errors = 0

    for id in batch_ids:
        try:
            # Get the data using an API call and append to the table
            film_dict = get_movie_details(details_url, api_key, id)
            film = pd.DataFrame(film_dict)

            film.to_sql('movie_data_raw', con, if_exists='append', index=False)
            batch_success += 1
        except Exception as e:
            batch_errors += 1
            continue
        
        processed_count += 1

        # Brief sleep to respect rate limits
        time.sleep(0.5)

    print(batch_success, batch_errors)

    # Commit periodically within batch
    if processed_count % COMMIT_FREQUENCY == 0:
        con.commit()

con.close()