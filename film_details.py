import requests

def get_movie_details(details_url, api_key, ids):
    """
    Get information about movies using the TMDB ids 
    """
    # List to hold the dictionaries of film details
    film_details = []

    # API calls for each movie in the list
    for id in ids:
        film_url = f"{details_url}{id}"
        r = requests.get(film_url, params={'api_key': api_key})
        film_raw = r.json()

        film_dict = {
            'name': film_raw['title'],
            'budget': film_raw['budget'],
            'genre': film_raw['genres'][0]['name'],
            'production_countries': film_raw['production_countries'][0]['name'],
            'revenue': film_raw['revenue'],
            'vote_average': film_raw['vote_average'],
            'release_year': int(film_raw['release_date'][:4])
        }

        film_details.append(film_dict)

    return film_details
