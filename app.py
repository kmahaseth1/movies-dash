import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
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
films = films[films['budget'] != 0]
"""

# Temporary data to setup the dashboard
# Convert the temp data from a list of a data frame and clean the DF
films = pd.DataFrame(temp_data)
films['release_year'] = films['release_year'].astype(str)
films = films[films['budget'] != 0]

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
cum_rev = films['revenue'].sum() / 1000000
total_films = len(films['name'])

genre_data = films.groupby(['release_year', 'genre']).size().reset_index(
    name='count'
)
genre_data['prop'] = genre_data.groupby('release_year')['count'].transform(
    lambda x: x / x.sum()
)

years = films['release_year'].sort_values().unique()
genres = films['genre'].sort_values().unique()
types = films['type'].sort_values().unique()
countries = films['production_countries'].sort_values().unique()

colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 
                  len(years), colortype='rgb')

# Create a Dash object and set its title
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Films Dashboard by Kushagra Mahaseth"

# Create graphs for the dashboard
fig2 = px.bar(films.sort_values(by="revenue", ascending=False).head(10), 
            x="name", y="revenue", title="Highest Grossing Movies",
            labels={'name': 'Film', 'revenue': 'Revenue'})
fig2.update_layout(title_x=0.5, title_font_size=24, 
                   title_font=dict(color='#4c9f95'),
                   xaxis_title_font_size=16,
                   xaxis_title_font=dict(color='#4c9f95'),
                   yaxis_title_font_size=16,
                   yaxis_title_font=dict(color='#4c9f95'),
                   plot_bgcolor='rgba(0,0,0,0)')
fig2.update_traces(marker_color='#4c9f95')
fig2.update_xaxes(tickfont=dict(color='#4c9f95'))
fig2.update_yaxes(tickfont=dict(color='#4c9f95'))

fig3 = px.bar(
    genre_data, 
    x='prop', y='release_year', color='genre', orientation='h', height = 300,
    title="Distribution of Genre of Released Films",
    labels={'prop': 'Proportion of Releases', 'release_year': 'Year'}
)
fig3.update_layout(title_x=0.5, title_font_size=24, 
                   title_font=dict(color='#4c9f95'),
                   xaxis_title_font_size=16,
                   xaxis_title_font=dict(color='#4c9f95'),
                   yaxis_title_font_size=16,
                   yaxis_title_font=dict(color='#4c9f95'),
                   plot_bgcolor='rgba(0,0,0,0)',
                   legend_title_font=dict(color='#4c9f95'),
                   legend=dict(font=dict(color='#4c9f95')))
fig3.update_xaxes(tickfont=dict(color='#4c9f95'))
fig3.update_yaxes(tickfont=dict(color='#4c9f95'))

fig4 = go.Figure()
for year, color in zip(years, colors):
    budget = films[films['release_year'] == year]['budget']

    fig4.add_trace(go.Violin(x=budget, line_color=color, name=str(year)))
fig4.update_traces(orientation='h', side='positive', width=3, points=False, 
                   meanline_visible=True)
fig4.update_layout(title="Budget Distribution by Year",
                   xaxis_title='Budget',
                   yaxis_title='Year',
                   title_x=0.5, title_font_size=24, 
                   title_font=dict(color='#4c9f95'),
                   xaxis_title_font_size=16,
                   xaxis_title_font=dict(color='#4c9f95'),
                   yaxis_title_font_size=16,
                   yaxis_title_font=dict(color='#4c9f95'),
                   plot_bgcolor='rgba(0,0,0,0)',
                   legend_title_font=dict(color='#4c9f95'),
                   legend=dict(font=dict(color='#4c9f95')))
fig4.update_xaxes(tickfont=dict(color='#4c9f95'))
fig4.update_yaxes(tickfont=dict(color='#4c9f95'))

fig5 = px.scatter(films, x="vote_average", y="revenue", text="name",
                title="Movie Quality vs Revenue", 
                labels={'vote_average': 'Average voter score', 
                        'revenue': 'Revenue'})
fig5.update_layout(title_x=0.5, title_font_size=24, 
                   title_font=dict(color='#4c9f95'),
                   xaxis_title_font_size=16,
                   xaxis_title_font=dict(color='#4c9f95'),
                   yaxis_title_font_size=16,
                   yaxis_title_font=dict(color='#4c9f95'),
                   plot_bgcolor='rgba(0,0,0,0)')
fig5.update_traces(mode="markers+text", textposition="top center", 
                   marker_color='#4c9f95', textfont=dict(color='#4c9f95', 
                                                         size=10))
fig5.update_xaxes(tickfont=dict(color='#4c9f95'))
fig5.update_yaxes(tickfont=dict(color='#4c9f95'))



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
                        html.Div(children="Year", className="menu-title"),
                        dcc.Dropdown(
                            id="year-filter",
                            options=[
                                {"label": year, "value": year}
                                for year in years
                            ],
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Genre", className="menu-title"),
                        dcc.Dropdown(
                            id="genre-filter",
                            options=[
                                {
                                    "label": genre.title(),
                                    "value": genre,
                                }
                                for genre in genres
                            ],
                            clearable=True,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
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
                        html.Div(children="Production Country", 
                                 className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {
                                    "label": country.title(),
                                    "value": country,
                                }
                                for country in countries
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
                html.Div(children=[
                        html.P("Highest Grossing Movie",
                            className="top"
            ),
                        html.P(f"{highest_grosser}",
                            className="bottom")
            ], className="box"),
                html.Div(children=[
                        html.P("Highest Rated Movie",
                            className="top"
            ),
                        html.P(f"{highest_scorer}",
                            className="bottom")
            ], className="box"), 
                html.Div(children=[
                        html.P("Leading Genre by Release Count",
                            className="top"
            ),
                        html.P(f"{most_pop_genre}",
                            className="bottom")
            ], className="box"), 
                html.Div(children=[
                        html.P("Total Revenue (in millions)",
                            className="top"
            ),
                        html.P(f"${cum_rev:,.0f} MM",
                            className="bottom")
            ], className="box"),
                html.Div(children=[
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
            dcc.Graph(id="genre-releases", className = "chart", 
                config={"displayModeBar": False}, 
                figure=fig3),
            dcc.Graph(id="budget-distribution", className = "chart",
                config={"displayModeBar": False}, 
                figure=fig4), 
            dcc.Graph(id="rev-vs-quality", className = "chart", 
                config={"displayModeBar": False}, 
                figure=fig5),   
            ], 
        className="charts")
    ]
) 

# Run the dashboard
if __name__ == "__main__":
    app.run(debug=True)
