import requests
import time

def get_movie_details(details_url, api_key, ids):
    """
    Get information about movies using the TMDB ids 
    """
    # List to hold the film details
    film_details = []

    # API calls for each movie in the list
    try:
        film_url = f"{details_url}{id}"
        r = requests.get(film_url, params={'api_key': api_key}, timeout=(10, 60))
        film_raw = r.json()
    except (requests.exceptions.JSONDecodeError) as e:
        return film_details

    # Extract other metrics
    film_dict = {
        'name': film_raw['title'],
        'budget': film_raw['budget'],
        'genres': [value['name'] for value in film_raw['genres']],
        'production_countries': film_raw['production_countries'][0]['name'] if film_raw['production_countries'] else None,
        'revenue': film_raw['revenue'],
        'vote_average': film_raw['vote_average'],
        'release_year': int(film_raw['release_date'][:4])
    } 

    film_dict['type'] = 'animation' if 'animation' in [x.lower() for x in film_dict['genres']] else 'live action'
    for genre in film_dict['genres']:
        if genre.lower() == "animation":
            continue
        else:
            film_dict['genre'] = genre.lower()
            break

    # Add the film to the list
    film_details.append(film_dict)

    return film_details
