import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import datetime
layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Artificial Intelligence Final Project", className="home-heading"
                ),
                html.P(
                    children="Team members:",
                    className="home-para",
                ),
                # Split up the above paragraph into multiple paragraphs
                html.P(
                    children = "Ricky Yucheng Cheng", className="home-para"
                ),
                html.P(
                    children = "Aayush Gandhi", className="home-para"
                ),
                html.P(
                    children = "Mark Rafael Gonzales", className="home-para"
                ),
                html.P(
                    children = "Nolan Scott Lombardo", className="home-para"
                ),
                html.P(
                    children = "Vivian Looi", className="home-para"
                ),
                html.P(
                    children = "Tyler Jinwoo Shin", className="home-para"
                ),
                html.Br(),
                html.P(
                    children='''The dashboard is built using Dash, a Python framework for building analytical web applications. 
                    The dashboard is hosted on Heroku, and the code can be made available.''',
                    className="home-para",
                ),
                html.Br(),
                html.P(
                    children='''Description of the Dashboard and all of the pages
                    ''',
                    className="home-para",
                ),
            ],
            className="header-home",
        )]
)