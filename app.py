import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import os
from dotenv import load_dotenv
from film_ids import get_ids_by_year
from film_details import get_movie_details
from temp_data import temp_data

"""
# Data processing
# API call setup
load_dotenv()
api_key = os.getenv("TMDB_API")
discover_url = "https://api.themoviedb.org/3/discover/movie"
details_url = "https://api.themoviedb.org/3/movie/"

# Get the movie ids
ids = []
start, end = 2020, 2025
for year in range(start, end + 1):
    yearly_ids = get_ids_by_year(discover_url, api_key, year)
    ids.append(yearly_ids)

# Extract movie details using get_movie_details
films_dict = get_movie_details(details_url, api_key, ids)

# Convert the dictionary into a DataFrame
films = pd.DataFrame(films_dict)
"""

# Temporary data to setup the dashboard
# Convert the temp data from a list of a data frame
films = pd.DataFrame(temp_data)

# Create a Dash object
app = Dash(__name__)

# Create graphs for the dashboard
fig1 = px.bar(films.sort_values(by="revenue", ascending=False), 
              x="name", y="revenue", title="Highest Grossing Movies",
              labels={'name': 'Film', 'revenue': 'Revenue'})
fig1.update_layout(title_x=0.5, title_font_size=24, xaxis_title_font_size=16,
                   yaxis_title_font_size=16)

fig2 = px.scatter(films, x="vote_average", y="revenue", text="name",
                  title="Movie Quality vs Revenue", 
                  labels={'vote_average': 'Average voter score', 
                          'revenue': 'Revenue'})
fig2.update_layout(title_x=0.5, title_font_size=24, xaxis_title_font_size=16,
                   yaxis_title_font_size=16)
fig2.update_traces(mode="markers+text", textposition="top center")

# Define the dashboard layout
app.layout = html.Div(
    children=[
        html.H1(children="2020s in Film"),
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
    ]
)

# Run the dashboard
if __name__ == "__main__":
    app.run(debug=True)
