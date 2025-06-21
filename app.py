import pandas as pd
from dash import Dash, dcc, html

# import data
# Define time frame for the data pull
begin = 2020
end = 2025

# Call the get_ids_by_year function to get all the movie ids for 2020s
tmdb_ids = []
for year in range(begin, end+1):
    year_ids = get_ids_by_year(year)
    tmdb_ids.extend(year_ids)

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