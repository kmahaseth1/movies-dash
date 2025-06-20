import requests
import os
from dotenv import load_dotenv
import time

# API call setup
load_dotenv()
api_key = os.getenv("TMDB_API")
base_url = "https://api.themoviedb.org/3/movie/"

# Small list of ids to check if the api call works 
# REPLACE WITH ID LIST film_ids.py ONCE THE CODE IS VALIDATED
# ids = [135397, 150540, 150689, 216015, 177677]
id = [177677]


def get_movie_details(ids):
    """
    Get information about movies using the TMDB ids 
    """
    # List to hold the dictionaries of film details
    film_details = []

    # API calls for each movie in the list
    for id in ids:
        film_url = f"{base_url}{id}"
        r = requests.get(film_url, params={'api_key': api_key})
        film_raw = r.json()

        film_dict = {
            'name': film_raw['title'],
            'budget': film_raw['budget'],
            'genre': film_raw['genres'][0]['name'],
            'production_countries': film_raw['production_countries'][0]['name'],
            'revenue': film_raw['revenue'],
            'vote_average': film_raw['vote_average']
        }

        film_details.append(film_dict)

    return film_dict

# check with one id
film_deets = get_movie_details(id)
print(film_deets)







        
    


    


