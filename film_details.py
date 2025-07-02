import requests
import time

def get_movie_details(details_url, api_key, ids):
    """
    Get information about movies using the TMDB ids 
    """
    # List to hold the film details
    film_details = []

    for id in ids:
        # API calls for each movie in the list
        try:
            film_url = f"{details_url}{id}"
            r = requests.get(film_url, params={'api_key': api_key}, timeout=(10, 60))
            film_raw = r.json()
        except (requests.exceptions.JSONDecodeError) as e:
            continue

        # Extract other metrics
        film_dict = {
            'name': film_raw['title'],
            'budget': film_raw['budget'],
            'type': 'live action',
            'genre': None,
            # 'genre': film_raw['genres'][0]['name'] if film_raw['genres'] else None,
            'production_countries': film_raw['production_countries'][0]['name'] if film_raw['production_countries'] else None,
            'revenue': film_raw['revenue'],
            'vote_average': film_raw['vote_average'],
            'release_year': int(film_raw['release_date'][:4])
        }

        # Get genre and film type
        for i, film in enumerate(film_raw['genres']):
            if film['genres'] and film.get("genres", "").lower() == "animation":
                film_dict['type'] = 'animation'
                if i + 1 < len(film['genres']):
                    film_dict['genre'] = film['genres'][i + 1].get("genres")
                break

        # Add the film to the list
        film_details.append(film_dict)

        # Brief sleep to respect rate limits
        time.sleep(0.1)

    return film_details
