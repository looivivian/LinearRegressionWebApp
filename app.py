import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
from pages import navbar, home, explore, relationships, experiment

from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE,
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    }],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

app.config.suppress_callback_exceptions = True

app.title = "Artifical Intelligence Final Project"

# df read json from data.json

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar.layout,
    html.Div(id='page-content', children=[]), 
    ]
)

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/explore':
        return explore.layout
    elif pathname == '/relationships':
        return relationships.layout
    elif pathname == '/experiment':
        return experiment.layout
    else:
        return home.layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)