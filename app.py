import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
import sqlite3

#Connect to the database
con = sqlite3.connect('movies_2020s.db')
films = pd.read_sql(
    '''
    SELECT * FROM movie_data_raw
    WHERE name IS NOT NULL
        AND budget > 0
        AND genre IS NOT NULL
        AND vote_average > 0
        AND release_year IS NOT NULL
        AND revenue > 0
        AND production_country IS NOT NULL
    ''',
    con
)

con.close()
# Set the variable to toggle cards and charts' colors
dash_color = '#4c9f95'

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
years = films['release_year'].sort_values().unique()
genres = films['genre'].sort_values().unique()
types = films['type'].sort_values().unique()
countries = films['production_country'].sort_values().unique()

# Create a Dash object and set its title
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Films Dashboard by Kushagra Mahaseth"

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
                        html.P(
                            id="highest-grosser", className="bottom")
            ], className="box"),
                html.Div(children=[
                        html.P("Highest Rated Movie",
                            className="top"
            ),
                        html.P(
                            id="highest-rated", className="bottom")
            ], className="box"), 
                html.Div(children=[
                        html.P(id="lead-genre", className="top"
            ),
                        html.P(
                            id="most-pop-genre", className="bottom")
            ], className="box"), 
                html.Div(children=[
                        html.P("Total Revenue (in millions)",
                            className="top"
            ),
                        html.P(
                            id="total-rev", className="bottom")
            ], className="box"),
                html.Div(children=[
                        html.P("Total Movies Released",
                            className="top"
            ),
                        html.P(
                            id="total-films", className="bottom")
            ], className="box"),
        ], className= "kpis"
        ),
        html.Div([     
            dcc.Graph(id="top-grossers", className = "chart",
                config={"displayModeBar": False}),
            dcc.Graph(id="genre-releases", className = "chart", 
                config={"displayModeBar": False}),
            dcc.Graph(id="budget-distribution", className = "chart",
                config={"displayModeBar": False}), 
            dcc.Graph(id="rev-vs-quality", className = "chart", 
                config={"displayModeBar": False}),   
            ], 
        className="charts")
    ]
) 

# Define callback functions to make the filters interactive
@app.callback(
    Output("highest-grosser", "children"),
    Output("highest-rated", "children"),
    Output("most-pop-genre", "children"),
    Output("total-rev", "children"),
    Output("total-films", "children"),
    Output("lead-genre", "children"),
    Output("top-grossers", "figure"),
    Output("genre-releases", "figure"),
    Output("budget-distribution", "figure"),
    Output("rev-vs-quality", "figure"),
    Input("year-filter", "value"),
    Input("genre-filter", "value"),
    Input("type-filter", "value"),
    Input("country-filter", "value")
)
def update_kpis_and_chart(year, genre, type, country):
    """
    # Open a SQLite connection
    with sqlite3.connect('movies_2020s.db') as con:
        query = '''
                SELECT * FROM movie_data_raw
                WHERE name IS NOT NULL
        '''
        films = pd.read_sql(query, con)
    """    
    filtered = films.copy()

    if year is not None:
        filtered=filtered[filtered['release_year']==year]
                     
    if genre is not None:
        filtered=filtered[filtered['genre']==genre]

    if type is not None:
        filtered=filtered[filtered['type']==type]  
                     
    if country is not None:
        filtered=filtered[filtered['production_country']==country]
    
    if filtered.empty:
        return (
            "No data available",
            "No data available",
            "No data available",
            "No data available",
            "No data available",
            px.bar(),
            px.bar(),
            go.Figure(),
            px.scatter()
        )
    
    # KPI card calculations and titles
    highest_grosser = filtered.loc[filtered['revenue'].idxmax(), 'name']
    highest_scorer = filtered.loc[filtered['vote_average'].idxmax(), 'name']
    most_pop_genre = filtered['genre'].value_counts().idxmax().title()
    cum_rev = filtered['revenue'].sum() / 1000000
    total_films = len(filtered['name'])
    genre_card_top="Leading Genre by Release Count"

    # Create figures
    genre_data = filtered.groupby(['release_year', 'genre']).size().reset_index(
        name='count'
    )
    genre_data['prop'] = genre_data.groupby('release_year')['count'].transform(
    lambda x: x / x.sum()
    )

    colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 
                  len(years), colortype='rgb')

    fig2 = px.bar(filtered.sort_values(by="revenue", ascending=False).head(10), 
            x="name", y="revenue", title="Highest Grossing Movies",
            labels={'name': 'Film', 'revenue': 'Revenue'})
    fig2.update_layout(title_x=0.5, title_font_size=24, 
                   title_font=dict(color=dash_color),
                   xaxis_title_font_size=16,
                   xaxis_title_font=dict(color=dash_color),
                   yaxis_title_font_size=16,
                   yaxis_title_font=dict(color=dash_color),
                   plot_bgcolor='rgba(0,0,0,0)')
    fig2.update_traces(marker_color=dash_color)
    fig2.update_xaxes(tickfont=dict(color=dash_color))
    fig2.update_yaxes(tickfont=dict(color=dash_color))
    
    if year is None and genre is None:
        fig3 = px.bar(
            genre_data, 
            x='prop', y='release_year', color='genre', orientation='h', 
            height = 400,
            title="Distribution of Genre of Released Films",
            labels={'prop': 'Proportion of Releases', 'release_year': 'Year'}
        )
        fig3.update_layout(title_x=0.5, title_font_size=24, 
                    title_font=dict(color=dash_color),
                    xaxis_title_font_size=16,
                    xaxis_title_font=dict(color=dash_color),
                    yaxis_title_font_size=16,
                    yaxis_title_font=dict(color=dash_color),
                    plot_bgcolor='rgba(0,0,0,0)',
                    legend_title_font=dict(color=dash_color),
                    legend=dict(font=dict(color=dash_color)))
        fig3.update_xaxes(tickfont=dict(color=dash_color))
        fig3.update_yaxes(tickfont=dict(color=dash_color))
    elif year is not None:
        fig3 = px.pie(genre_data, values='prop', names="genre",
                      title="Distribution of Genre of Released Films", 
                      hole=0.5, height=600)
        fig3.update_layout(title_x=0.5, title_font_size=24, 
                    title_font=dict(color=dash_color))
    elif genre is not None:
        fig3 = px.bar(
            filtered.groupby('release_year').size().reset_index(name="count"), 
            x='count', y='release_year',
            height = 300,
            title=f"{genre.title()} movies release pattern",
            labels={'count': 'Number of Movies Released', 
                    'release_year': 'Year'}
        )
        fig3.update_layout(title_x=0.5, title_font_size=24, 
                    title_font=dict(color=dash_color),
                    xaxis_title_font_size=16,
                    xaxis_title_font=dict(color=dash_color),
                    yaxis_title_font_size=16,
                    yaxis_title_font=dict(color=dash_color),
                    plot_bgcolor='rgba(0,0,0,0)',
                    legend_title_font=dict(color=dash_color),
                    legend=dict(font=dict(color=dash_color)))
        fig3.update_traces(marker_color=dash_color)
        fig3.update_xaxes(tickfont=dict(color=dash_color))
        fig3.update_yaxes(tickfont=dict(color=dash_color))
        genre_card_top = f"Viewing data on"
        most_pop_genre = f"{most_pop_genre} movies"

    fig4 = go.Figure()
    for y, color in zip(years, colors):
        budget = filtered[filtered['release_year'] == y]['budget']

        fig4.add_trace(go.Violin(x=budget, line_color=color, name=str(y)))
    fig4.update_traces(orientation='h', side='positive', width=3, points=False, 
                   meanline_visible=True)
    fig4.update_layout(title="Budget Distribution by Year",
                   xaxis_title='Budget',
                   yaxis_title='Year',
                   title_x=0.5, title_font_size=24, 
                   title_font=dict(color=dash_color),
                   xaxis_title_font_size=16,
                   xaxis_title_font=dict(color=dash_color),
                   yaxis_title_font_size=16,
                   yaxis_title_font=dict(color=dash_color),
                   plot_bgcolor='rgba(0,0,0,0)',
                   legend_title_font=dict(color=dash_color),
                   legend=dict(font=dict(color=dash_color)))
    fig4.update_xaxes(tickfont=dict(color=dash_color))
    fig4.update_yaxes(tickfont=dict(color=dash_color))

    fig5 = px.scatter(filtered, x="vote_average", y="revenue",
                title="Voter Score vs. Log-Transformed Revenue", 
                labels={'vote_average': 'Average voter score', 
                        'revenue': 'Log of Revenue'}, opacity=0.4,
                        log_y=True)
    fig5.update_layout(title_x=0.5, title_font_size=24, 
                   title_font=dict(color=dash_color),
                   xaxis_title_font_size=16,
                   xaxis_title_font=dict(color=dash_color),
                   yaxis_title_font_size=16,
                   yaxis_title_font=dict(color=dash_color),
                   plot_bgcolor='rgba(0,0,0,0)')
    fig5.update_traces(textposition="top center", marker=dict(size=7.5),
                   marker_color=dash_color, textfont=dict(color=dash_color, 
                                                         size=10))
    fig5.update_xaxes(tickfont=dict(color=dash_color))
    fig5.update_yaxes(tickfont=dict(color=dash_color))

    return (
        f"{highest_grosser}", f"{highest_scorer}", f"{most_pop_genre}", 
        f"${cum_rev:,.0f} MM", f"{total_films:,}", genre_card_top, 
        fig2, fig3, fig4, fig5)
        
# Run the dashboard
if __name__ == "__main__":
    app.run(debug=True)
