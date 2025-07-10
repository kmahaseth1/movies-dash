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
"""

con = sqlite3.connect('movies_2020s.db')
cursor = con.cursor()

cursor.execute("DROP TABLE IF EXISTS movie_data_raw")
con.commit()
con.close()

"""
# See the data table
con = sqlite3.connect('movies_2020s.db')
cursor = con.cursor()
cursor.execute('''
               SELECT * FROM movie_data_raw
               WHERE name like 'The Wild Robot'
               ''')
rows = cursor.fetchall()
# Print the results
for row in rows:
    print(row)

con.close()
"""