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

# Define time frame for the data pull
begin = 2020
end = 2025

# Call the get_ids_by_year function to get all the movie ids for 2020s
tmdb_ids = []
for year in range(begin, end+1):
    year_ids = get_ids_by_year(discover_url, api_key, year)
    tmdb_ids.extend(year_ids)

# Extract movie details using get_movie_details
films = get_movie_details(details_url, api_key, tmdb_ids)

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