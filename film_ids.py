import requests
import time

def get_ids_by_year(discover_url, api_key, year):
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
        r = requests.get(discover_url, params=parameters)
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