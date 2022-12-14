import dash
from dash import html, dcc, callback, Input, Output, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime
import plotly.express as px

# Open the datasets folder and read the csv files
# The title of the csv file is the name of the dataset
import os
fileNames = os.listdir("datasets")
FileNameEnum = {
    "fifa.csv": "FIFA 2022 World Cup Data",
    "housing.csv": "Boston Housing Data",
    "avocado.csv": "Avocado Prices Data",
    "happiness.csv": "World Happiness Report 2019",
}

defaultOptions = []
for file in fileNames:
    defaultOptions.append({"label": FileNameEnum[file], "value": file})

layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Explore Custom Parameters", className="header-title"
                ),
                html.P(
                    children="This page allows you to explore the custom parameters of the linear regression model.",
                    className="header-description",
                ),
                html.Div(dcc.Markdown('''
                * Each dataset is imported from Kaggle.com and contains a variety of data points
                * The data is cleaned and formatted to be used in the app
                * The data is then used to create a custom linear regression model
                ''', mathjax=True),className="header-description",),
                # Split the above div up into 4 P blocks
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Select a Dataset", className="menu-title"),
                        dcc.Dropdown(
                            id="input-filter-experiment",
                            options=defaultOptions,
                            value="happiness.csv",
                            clearable=False,
                        ),
                        
                    html.Div(id="warning", className="menu-title"),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Choose X Axis Variable", className="menu-title"),
                        dcc.Dropdown(
                            id="output-filter-experiment",
                            options=defaultOptions,
                            clearable=False,
                            searchable=False,
                            className="dropdown-multi",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Choose Y Axis Variable", className="menu-title"),
                        dcc.Dropdown(
                            id="output-filter2-experiment",
                            options=defaultOptions,
                            
                            clearable=False,
                            searchable=False,
                            className="dropdown-multi",
                        ),
                        
                    ],
                ),

                html.Div(
                    children=[
                        html.Div(children="Enter Learning Rate", className="menu-title"),
                        dcc.Input(
                            id="learning-rate",
                            type="number",
                            placeholder="Enter Learning Rate",
                            value=0.001,
                            className="dropdown-multi",
                        ),
                        html.Div(children="Epochs", className="menu-title"),
                        dcc.Input(
                            id="iterations",
                            type="number",
                            placeholder="Enter Number of Iterations",
                            value=100,
                            className="dropdown-multi",
                        ),
                    ],
                ),
                

            ],
            className="menu-experiment",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="experiment-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": 0,
                                    "y": 0,
                                    "type": "lines",
                                    "hovertemplate": " Y = %{y:.2f} X + %{x:.2f}<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Relationship between Selected Input and Time",
                                    "x": 0.1,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },


                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="cost-slope-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": 0,
                                    "y": 0,
                                    "type": "lines",
                                    "hovertemplate": " Y = %{y:.2f} X + %{x:.2f}<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Relationship between Cost Function and Slope",
                                    "x": 0.1,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },


                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="cost-intercept-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": 0,
                                    "y": 0,
                                    "type": "lines",
                                    "hovertemplate": " Y = %{y:.2f} X + %{x:.2f}<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Relationship between Cost Function and Y-Intercept",
                                    "x": 0.1,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },


                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="cost-iterations-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": 0,
                                    "y": 0,
                                    "type": "lines",
                                    "hovertemplate": " Y = %{y:.2f} X + %{x:.2f}<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Relationship between Cost Function and Iterations of Gradient Descent",
                                    "x": 0.1,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },


                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        # html.Div(
        #     children=[
        #         # Display the data from the graph
        #         # such as the equation of the line
        #         # and the correlation coefficien
        #         html.Div(
        #             children=[
        #                 html.Div(children="Equation of the line", className="menu-title"),
        #                 html.Div(id="equation-experiment", className="warning"),
        #             ]
        #         ),
        #         # Pearson correlation coefficient
        #         html.Div(
        #             children=[
        #                 html.Div(children="Pearson correlation coefficient", className="menu-title"),
        #                 html.Div(id="correlation-experiment", className="warning"),
                        
        #             ]
        #         ),
        #         # pvalue
        #         html.Div(
        #             children=[
        #                 html.Div(children="P-value", className="menu-title"),
        #                 html.Div(id="pvalue-experiment", className="warning"),
                        
        #             ]
        #         ),
        #         # Standard error of the estimated slope
        #         html.Div(
        #             children=[
        #                 html.Div(children="Standard error of the estimated slope", className="menu-title"),
        #                 html.Div(id="standard_error-experiment", className="warning"),
                        
        #             ]
        #         ),
        #         # intercept_stderr
        #         html.Div(
        #             children=[
        #                 html.Div(children="Standard error of the estimated intercept", className="menu-title"),
        #                 html.Div(id="intercept_stderr-experiment", className="warning"),
                        
        #             ]
        #         ),



        #     ],
        #     className="menu-explore-data-experiment",
        # ),
    ],  
    
)


# Depending on the dataset selected, the dropdown menu will change
# The dropdown menu will only show the columns that are in the dataset
@callback(
    Output("output-filter-experiment", "options"),
    [Input("input-filter-experiment", "value")],
)
def set_output_options(input_value):
    df = pd.read_csv("datasets/" + input_value)
    options = []
    for col in df.columns:
        if df[col].dtype == "int64" or df[col].dtype == "float64":
            if input_value == "housing.csv":
                # col is just the first name before _
                colOriginal = col
                colName = col.split("_")[0]
                options.append({"label": colName, "value": colOriginal})
                continue
            else:
                colOriginal = col
                col = col.replace("_", " ").title()
                options.append({"label": col, "value": colOriginal})
    return options

@callback(
    Output("output-filter2-experiment", "options"),
    [Input("input-filter-experiment", "value")],
)
def set_output_options(input_value):
    df = pd.read_csv("datasets/" + input_value)
    
    options = []
    for col in df.columns:
        # Only if the column contains numeric data
        if df[col].dtype == "int64" or df[col].dtype == "float64":
            if input_value == "housing.csv":
                # col is just the first name before _
                colOriginal = col
                colName = col.split("_")[0]
                options.append({"label": colName, "value": colOriginal})
                continue
            else:
                colOriginal = col
                col = col.replace("_", " ").title()
                options.append({"label": col, "value": colOriginal})
    return options


# If no options have been selected for the dropdown menu, select any two options at random
@callback(
    Output("output-filter-experiment", "value"),
    [Input("output-filter-experiment", "options")],
)
def set_output_value(available_options):
    if available_options:
        return available_options[0]["value"]
    else:
        return None

@callback(
    Output("output-filter2-experiment", "value"),
    [Input("output-filter2-experiment", "options")],
)
def set_output_value(available_options):
    if available_options:
        return available_options[1]["value"]
    else:
        return None

def gradient_descent(x_column, y_column, learning_rate, iterations):
    # if learning_rate is None or 0, set it to 0.01
    if learning_rate is None or learning_rate == 0:
        learning_rate = 0.01
    import numpy as np
    m= 0
    b = 0
    costs = []
    m_list = []
    b_list = []
    x_values = x_column
    y_values = y_column
    n = len(x_values)
    for iteration in range(iterations):
        y_guess = m * x_values + b
        cost = (1 / n) * (1/n) * np.sum((y_values - y_guess)**2)
        costs.append(cost)

        gradientM = -(2/n) * np.sum(x_values * (y_values - y_guess))
        gradientB = -(2/n) * np.sum(y_values - y_guess)
        m = m - (learning_rate * gradientM)
        b = b - (learning_rate * gradientB)
        m_list.append(m)
        b_list.append(b)

    return m, b, costs, m_list, b_list

@callback(
    [
    Output("experiment-chart", "figure"),
    Output("cost-slope-chart", "figure"),
    Output("cost-intercept-chart", "figure"),
    Output("cost-iterations-chart", "figure"),
    ],
    [
        Input("input-filter-experiment", "value"),
        Input("output-filter-experiment", "value"),
        Input("output-filter2-experiment", "value"),
        Input("iterations", "value"),
        Input("learning-rate", "value"),
    ],
)
def set_chart(input_value, output_value, output_value2, iterations, learning_rate):
    # Display the data from the graph
    df = pd.read_csv("datasets/" + input_value)
    x_column = df[output_value]
    y_column = df[output_value2]
    output_value = output_value.replace("_", " ").title()
    output_value2 = output_value2.replace("_", " ").title()
    df = pd.read_csv("datasets/" + input_value)
    # remove nan values and the corresponding y values
    import numpy as np
    x_column = x_column[~np.isnan(x_column)]
    y_column = y_column[~np.isnan(y_column)]
    # Fix the columns so they are the same length
    if len(x_column) > len(y_column):
        x_column = x_column[:len(y_column)]
    elif len(y_column) > len(x_column):
        y_column = y_column[:len(x_column)]

    # Get the Linear Regression model using Gradient Descent
    m, b, costs, m_list, b_list = gradient_descent(x_column, y_column, learning_rate, iterations)
    # Plot the data and the line that was found
    import plotly.graph_objects as go
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_column, y=y_column, mode="markers", name="Data"))
    fig.add_trace(go.Scatter(x=x_column, y=m * x_column + b, mode="lines", name="Regression Line"))
    fig.update_layout(
        title="Linear Regression using Gradient Descent",
        xaxis_title=output_value,
        yaxis_title=output_value2,
    )
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=m_list, y=costs, mode="lines", name="Cost"))
    fig2.update_layout(
        title="Cost vs Slope",
        xaxis_title="Slope",
        yaxis_title="Cost",
        # Set the x limits to the min and max of the slope list
        xaxis_range=[min(m_list), max(m_list)],

    )
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=b_list, y=costs, mode="lines", name="Cost"))
    fig3.update_layout(
        title="Cost vs Intercept",
        xaxis_title="Intercept",
        yaxis_title="Cost",
        # Set the x limits to the min and max of the slope list
        xaxis_range=[min(b_list), max(b_list)],
    )
    fig4 = go.Figure()
    xRange = np.linspace(0, iterations, iterations)
    fig4.add_trace(go.Scatter(x=xRange, y=costs, mode="lines", name="Cost"))
    fig4.update_layout(
        title="Cost vs Iterations",
        xaxis_title="Iterations",
        yaxis_title="Cost",
    )
    return [fig, fig2, fig3, fig4]
