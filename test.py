import sqlite3
import pandas as pd
from film_details import get_movie_details
import os
from dotenv import load_dotenv

"""
id = 747358
load_dotenv()
api_key = os.getenv("TMDB_API")
details_url = "https://api.themoviedb.org/3/movie/"

film_dict = get_movie_details(details_url, api_key, id)
film = pd.DataFrame(film_dict)

print(film)

con = sqlite3.connect('movies_2020s.db')

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
film.to_sql('movie_data_raw', con, if_exists='append', index=False)

cursor = con.cursor()

#cursor.execute('SELECT production_countries FROM movie_data_raw')

#cursor.execute('DELETE FROM movie_data_raw')
#con.commit()

rows = cursor.fetchall()
# Print the results
for row in rows:
    print(row)

con.close()


con = sqlite3.connect('movies_2020s.db')
cursor = con.cursor()

cursor.execute("DROP TABLE IF EXISTS movie_data_raw")
con.commit()
con.close()


# See the data table
con = sqlite3.connect('movies_2020s.db')
cursor = con.cursor()
cursor.execute('''
               SELECT * FROM movie_data_raw
               LIMIT 100
               ''')
rows = cursor.fetchall()
# Print the results
for row in rows:
    print(row)

con.close()


# Path to your SQLite database file
db = 'movies_2020.db'

# Connect to the database (just to ensure it's not open)
try:
    con = sqlite3.connect(db)
    con.close()
    print(f"Successfully connected to {db}.")
except sqlite3.Error as e:
    print(f"Error while connecting to database: {e}")

# Now delete the database file
if os.path.exists(db):
    os.remove(db)
    print(f"Database file '{db}' deleted successfully.")
else:
    print(f"Database file '{db}' does not exist.")
"""

# Connect to your database
con = sqlite3.connect('movies_2020s.db')
cursor = con.cursor()

df = pd.read_sql_query("SELECT * FROM movie_data_raw", con)

"""
# Display as a table
countries = list(df['production_country2'].unique())
for i, country in enumerate(countries):
    print(f"{i}. {country}")
"""
df = pd.read_sql(
    '''
    SELECT * FROM movie_data_raw
    WHERE name IS NOT NULL
        AND genre IS NOT NULL
        AND genre <> 'Documentary'
        AND release_year IS NOT NULL
        AND TRIM(release_year) <> ''
        AND TRIM(genre) <> ''
        AND budget > 50000
        AND production_country2 = 'United States'
        AND name = 'Dinosaur Train: Adventure Island'
    ''',
    con
)
print(df.head())