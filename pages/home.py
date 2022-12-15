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
                html.P(
                    children = "Ricky Yucheng Cheng, Aayush Gandhi, Mark Rafael Gonzales, Nolan Scott Lombardo, Vivian Looi, Tyler Jinwoo Shin", className="home-para"
                ),
                html.Br(),
                html.P(
                    children=['''The dashboard is built using Dash, a Python framework for building analytical web applications. 
                    The dashboard is hosted on Render.com, and code for the dashboard is available on ''',
                    html.A(
                        children="GitHub",
                        href="https://github.com/looivivian/LinearRegressionWebApp"
                    )
                    ],
                    className="home-para",
                ),
                html.Br(),
                html.P(
                    children=['''Our solution to demonstrate Linear Regression is split into 3 parts: ''',
                    '''The first page, the Home page, is where you are now. ''',
                    '''The second page, the Explore page, is where you can view the data that you upload in a particular format. ''',
                    '''The analysis on the Explore page is done using the scikit-learn library and is optimized for speed and accuracy. ''',
                    '''The third page, the Relationships page, is where you can look at preexisting relationships between the some popular datasets. ''',
                    '''Again the analysis on the Relationships page is done using the scikit-learn library and is optimized for speed and accuracy. ''',
                    '''Finally, the fourth page, the Experiment page, is where you can upload your own data and see the results of the analysis using Gradient Descent and concepts of Machine Learning. ''',
                    '''The analysis on the Experiment page is done using manually coded algorithms and allows to alter the results produced by the Explore page. ''',

                    ],

                    className="home-para",
                ),
            ],
            className="header-home",
        )]
)