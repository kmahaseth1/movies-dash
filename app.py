import pandas as pd
from dash import Dash, dcc, html
import os
from dotenv import load_dotenv
from film_ids import get_ids_by_year
from film_details import get_movie_details

# Data processing
# API call setup
load_dotenv()
api_key = os.getenv("TMDB_API")
discover_url = "https://api.themoviedb.org/3/discover/movie"
details_url = "https://api.themoviedb.org/3/movie/"

# Get the movie ids
ids = get_ids_by_year(discover_url, api_key, 2025)

# Extract movie details using get_movie_details
films = get_movie_details(details_url, api_key, ids)

print(films[:10])

"""
# Create a Dash object
app = Dash(__name__)

# Define the dashboard layout
app.layout = html.Div(
    children=[
        html.H1(children="2020s in Film")
    ]
)

# Run the dashboard
if __name__ == "__main__":
    app.run(debug=True)
"""