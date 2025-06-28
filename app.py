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
films['release_year'] = films['release_year'].astype(str)

# Import an external CSS file containing necessary font family
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Summary datasets and stats
highest_grosser = films.loc[films['revenue'].idxmax(), 'name']
highest_scorer = films.loc[films['vote_average'].idxmax(), 'name']
most_pop_genre = films['genre'].value_counts().idxmax()
cum_rev = films['revenue'].sum()
total_films = len(films['name'])

# Create a Dash object and set its title
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Films Dashboard by Kushagra Mahaseth"

# Create graphs for the dashboard
fig2 = px.bar(films.sort_values(by="revenue", ascending=False), 
            x="name", y="revenue", title="Highest Grossing Movies",
            labels={'name': 'Film', 'revenue': 'Revenue'})
fig2.update_layout(title_x=0.5, title_font_size=24, xaxis_title_font_size=16,
                   yaxis_title_font_size=16)

fig3 = px.scatter(films, x="vote_average", y="revenue", text="name",
                  title="Movie Quality vs Revenue", 
                  labels={'vote_average': 'Average voter score', 
                          'revenue': 'Revenue'})
fig3.update_layout(title_x=0.5, title_font_size=24, xaxis_title_font_size=16,
                   yaxis_title_font_size=16)
fig3.update_traces(mode="markers+text", textposition="top center")

# Define the dashboard layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="2020s in Film", className="header-title"),
                 ], className="header"
        ),
        html.Div(
            children=[
                html.P(children=[
                        html.P("Highest Grossing Film",
                            className="box top", id="one"
            ),
                        html.P(f"{highest_grosser}",
                            className="box bottom", id="one")
            ]),
                html.P(children=[
                        html.P("Highest Rated Film",
                            className="box top", id="two"
            ),
                        html.P(f"{highest_scorer}",
                            className="box bottom")
            ]), 
                html.P(children=[
                        html.P("Most Popular Genre",
                            className="box top"
            ),
                        html.P(f"{most_pop_genre}",
                            className="box bottom")
            ]), 
                html.P(children=[
                        html.P("Cumulative Revenue",
                            className="box top"
            ),
                        html.P(f"${cum_rev:,.0f}",
                            className="box bottom")
            ]),
                html.P(children=[
                        html.P("Total Movies Released",
                            className="box top"
            ),
                        html.P(f"{total_films}",
                            className="box bottom")
            ]),
        ], className= "kpis"
        ),       
        dcc.Graph(id="top-grossers",
                config={"displayModeBar": False}, 
                figure=fig2),
        dcc.Graph(id="rev-vs-quality",
                config={"displayModeBar": False}, 
                figure=fig3),     
    ]
)

# Run the dashboard
if __name__ == "__main__":
    app.run(debug=True)
