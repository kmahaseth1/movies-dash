from film_ids import get_ids_by_year
import os
from dotenv import load_dotenv
import pandas as pd
import csv

load_dotenv()
api_key = os.getenv("TMDB_API")
discover_url = "https://api.themoviedb.org/3/discover/movie"
details_url = "https://api.themoviedb.org/3/movie/"

# Get the movie ids
ids = []
start, end = 2020, 2025
for year in range(start, end + 1):
    yearly_ids = get_ids_by_year(discover_url, api_key, year)
    ids.append(yearly_ids)

id_file = 'id_list.csv'

with open(id_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    for id in ids:
        csv_writer.writerow(id)
        