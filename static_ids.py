import os
from dotenv import load_dotenv
from film_ids import get_ids_by_year
import csv

# Get ids for movies from 2020-24
# API call setup
load_dotenv()
api_key = os.getenv("TMDB_API")
discover_url = "https://api.themoviedb.org/3/discover/movie"

# Define time frame for the data pull
begin, end = 2020, 2025

# Call the get_ids_by_year function to get all the movie ids for 2020s
tmdb_ids_20_24 = []
for year in range(begin, end):
    year_ids = get_ids_by_year(discover_url, api_key, year)
    tmdb_ids_20_24.extend(year_ids)

# Save the data
with open('data/static_ids.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for i in  tmdb_ids_20_24:
        writer.writerow([i])