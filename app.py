import pandas as pd
from dash import Dash, dcc, html

# import data from data.py

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