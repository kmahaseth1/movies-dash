import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table
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
films['release_year'] = films['release_year'].astype(str)
films['mkt_est'] = np.where(films['budget'] >= 100000000, 100000000, 35000000)
films['profits'] = films["revenue"] - (films["budget"] + films["mkt_est"])
films['profits_pct'] = films["revenue"] / films["budget"]
films['profits_pct'] = films['profits_pct'].replace([np.inf, -np.inf], np.nan)
"""

# Temporary data to setup the dashboard
# Convert the temp data from a list of a data frame
films = pd.DataFrame(temp_data)
films['release_year'] = films['release_year'].astype(str)
films['mkt_est'] = np.where(films['budget'] >= 100000000, 100000000, 35000000)
films['profits'] = films["revenue"] - (films["budget"] + films["mkt_est"])
films['profits_pct'] = films["profits"] / films["budget"]
films['profits_pct'] = films['profits_pct'].replace([np.inf, -np.inf], np.nan)

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

genre_data = films.groupby(['release_year', 'genre']).size().reset_index(
    name='count'
)
genre_data['prop'] = genre_data.groupby('release_year')['count'].transform(
    lambda x: x / x.sum()
)

top_profits = films.sort_values('profits_pct', ascending=False).head(10)

genres = films['genre'].sort_values().unique()
types = films['type'].sort_values().unique()
years = films['release_year'].sort_values().unique()

# Create a Dash object and set its title
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Films Dashboard by Kushagra Mahaseth"

# Create graphs for the dashboard
fig2 = px.bar(films.sort_values(by="revenue", ascending=False).head(10), 
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

fig4 = px.bar(
    genre_data, 
    x='prop', y='release_year', color='genre', orientation='h', height = 300,
    title="Distribution of Genre of Released Films",
    labels={'prop': 'Proportion of Releases', 'release_year': 'Year'}
)
fig4.update_layout(title_x=0.5, title_font_size=24, xaxis_title_font_size=16,
                   yaxis_title_font_size=16)

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
                html.Div(
                    children=[
                        html.Div(children="Genre", className="menu-title"),
                        dcc.Dropdown(
                            id="genre-filter",
                            options=[
                                {"label": genre.title(), "value": genre}
                                for genre in genres
                            ],
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": type.title(),
                                    "value": type,
                                }
                                for type in types
                            ],
                            clearable=True,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Year", className="menu-title"),
                        dcc.Dropdown(
                            id="year-filter",
                            options=[
                                {
                                    "label": year,
                                    "value": year,
                                }
                                for year in years
                            ],
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.P(children=[
                        html.P("Highest Grossing Film",
                            className="top"
            ),
                        html.P(f"{highest_grosser}",
                            className="bottom")
            ], className="box"),
                html.P(children=[
                        html.P("Highest Rated Film",
                            className="top"
            ),
                        html.P(f"{highest_scorer}",
                            className="bottom")
            ], className="box"), 
                html.P(children=[
                        html.P("Most Popular Genre",
                            className="top"
            ),
                        html.P(f"{most_pop_genre}",
                            className="bottom")
            ], className="box"), 
                html.P(children=[
                        html.P("Cumulative Revenue",
                            className="top"
            ),
                        html.P(f"${cum_rev:,.0f}",
                            className="bottom")
            ], className="box"),
                html.P(children=[
                        html.P("Total Movies Released",
                            className="top"
            ),
                        html.P(f"{total_films}",
                            className="bottom")
            ], className="box"),
        ], className= "kpis"
        ),
        html.Div([     
            dcc.Graph(id="top-grossers", className = "chart",
                config={"displayModeBar": False}, 
                figure=fig2),
            dcc.Graph(id="rev-vs-quality", className = "chart", 
                config={"displayModeBar": False}, 
                figure=fig3),
            dcc.Graph(id="genre-releases", className = "chart",
                config={"displayModeBar": False}, 
                figure=fig4),
            html.Div([
                html.P("Top Movies by Profit-to-Expense Ratio", 
                        className="table-title"),
                dash_table.DataTable(
                    id="profits-table",
                    data=top_profits.to_dict('records'),
                    columns=[
                        {'name': 'Movie Name', 'id': 'name'},
                        {'name': 'Release Year', 'id': 'release_year'},
                        {'name': 'Genre', 'id': 'genre'},
                        {'name': 'Profit (pct of  Budget)', 'id': 'profits_pct',
                            'type': 'numeric', 'format': {'specifier': '.0%'}}
                        ])
                ], className="chart"),      
            ], 
        className="charts")
    ]
) 

# Run the dashboard
if __name__ == "__main__":
    app.run(debug=True)
