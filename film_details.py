import requests
import json

def get_movie_details(details_url, api_key, id):
    """
    Get information about movies using the TMDB ids 
    """
    # List to hold the film details
    film_details = []

    # API calls for each movie in the list
    try:
        film_url = f"{details_url}{id}"
        r = requests.get(film_url, params={'api_key': api_key}, timeout=(60, 60))
        film_raw = r.json()
    except (requests.exceptions.JSONDecodeError) as e:
        return film_details

    # Extract other metrics
    film_dict = {
        'tmdb_id': id,
        'name': film_raw.get('title'),
        'budget': film_raw.get('budget'),
        'genres': json.dumps([value['name'] for value in film_raw.get('genres', [])]),
        'production_countries': json.dumps([value['name'] for value in film_raw.get('production_countries', [])]),
        'revenue': film_raw.get('revenue'),
        'vote_average': film_raw.get('vote_average'),
        'release_year': film_raw.get('release_date', '')[:4]
    } 
    genres = json.loads(film_dict['genres'])
    if 'Animation' in genres:
        film_dict['type'] = 'animation'
    else:
        film_dict['type'] = 'live action'
    
    for genre in genres:
        if genre.lower() == "animation":
            continue
        else:
            film_dict['genre'] = genre.title()
            break
    production_countries = json.loads(film_dict['production_countries'])
    if production_countries:
        if "United States of America" in production_countries:
            film_dict['production_country'] = "United States of America"
        else:
            film_dict['production_country'] = production_countries[0]
    else:
        film_dict['production_country'] = None

    # Add the film to the list
    film_details.append(film_dict)

    return film_details
