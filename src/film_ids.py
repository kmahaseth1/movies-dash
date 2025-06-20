import requests
import os
from dotenv import load_dotenv
import time

# API call setup
load_dotenv()
api_key = os.getenv("TMDB_API")
base_url = "https://api.themoviedb.org/3/discover/movie"

def get_ids_by_year(year):
    """
    Get the THDB ids for movies released in a specific year
    """

    ids = []
    page = 1
    total_pages = 1 # placeholder

    while page <= total_pages:
        # Specify API query parameters
        parameters = {
            'api_key': api_key,
            'primary_release_year': year,
            'page': page
        }

        # Send GET request to the /discover/movie endpoint
        r = requests.get(base_url, params=parameters)
        films = r.json()

        # If valid response, extract the ids, break otherwise 
        if 'results' in films:
            for film in films['results']:
                ids.append(film['id'])
        else:
            break

        # Update total pages after the first request
        if page == 1:
            total_pages = films['total_pages']
        
        # Increment the page number
        page += 1

        # Brief sleep to respect rate limits
        time.sleep(0.1)
    
    return ids

# Define time frame for the data pull
begin = 2020
end = 2025

# Call the get_ids_by_year function to get all the movie ids for 2020s
tmdb_ids = []
for year in range(begin, end+1):
    year_ids = get_ids_by_year(year)
    tmdb_ids.extend(year_ids)
