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
                    children="Explore Custom Datasets", className="header-title"
                ),
                html.P(
                    children="Select from a variety of datasets from the dropdown menu",
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
                            id="input-filter",
                            options=defaultOptions,
                            value="fifa.csv",
                            clearable=False,
                        ),
                        
                    html.Div(id="warning", className="menu-title"),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Choose X Axis Variable", className="menu-title"),
                        dcc.Dropdown(
                            id="output-filter",
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
                            id="output-filter2",
                            options=defaultOptions,
                            
                            clearable=False,
                            searchable=False,
                            className="dropdown-multi",
                        ),
                    ],
                ),
                        
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="relationship-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": 0,
                                    "y": 0,
                                    "type": "lines",
                                    "hovertemplate": " %{y:.2f}"
                                                     "<extra></extra>",
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
                # Display the data from the graph
                # such as the equation of the line
                # and the correlation coefficien
                html.Div(
                    children=[
                        html.Div(children="Equation of the line", className="menu-title"),
                        html.Div(id="equation-relation", className="warning"),
                    ]
                ),
                # Pearson correlation coefficient
                html.Div(
                    children=[
                        html.Div(children="Pearson correlation coefficient", className="menu-title"),
                        html.Div(id="correlation-relation", className="warning"),
                        
                    ]
                ),
                # pvalue
                html.Div(
                    children=[
                        html.Div(children="P-value", className="menu-title"),
                        html.Div(id="pvalue-relation", className="warning"),
                        
                    ]
                ),
                # Standard error of the estimated slope
                html.Div(
                    children=[
                        html.Div(children="Standard error of the estimated slope", className="menu-title"),
                        html.Div(id="standard_error-relation", className="warning"),
                        
                    ]
                ),
                # intercept_stderr
                html.Div(
                    children=[
                        html.Div(children="Standard error of the estimated intercept", className="menu-title"),
                        html.Div(id="intercept_stderr-relation", className="warning"),
                        
                    ]
                ),



            ],
            className="menu-explore-data",
        ),
    ],
    
)


# Depending on the dataset selected, the dropdown menu will change
# The dropdown menu will only show the columns that are in the dataset
@callback(
    Output("output-filter", "options"),
    [Input("input-filter", "value")],
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
    Output("output-filter2", "options"),
    [Input("input-filter", "value")],
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
    Output("output-filter", "value"),
    [Input("output-filter", "options")],
)
def set_output_value(available_options):
    if available_options:
        return available_options[0]["value"]
    else:
        return None

@callback(
    Output("output-filter2", "value"),
    [Input("output-filter2", "options")],
)
def set_output_value(available_options):
    if available_options:
        return available_options[1]["value"]
    else:
        return None

@callback(
    Output("relationship-chart", "figure"),
    [
        Input("input-filter", "value"),
        Input("output-filter", "value"),
        Input("output-filter2", "value"),
    ],
)
def set_chart(input_value, output_value, output_value2):    
    df = pd.read_csv("datasets/" + input_value)
    x_column = df[output_value]
    y_column = df[output_value2]
    output_value = output_value.replace("_", " ").title()
    output_value2 = output_value2.replace("_", " ").title()
    df = pd.read_csv("datasets/" + input_value)
    
    # Plot line of best fit
    import scipy.stats as stats
    # remove nan values and the corresponding y values
    import numpy as np
    x_column = x_column[~np.isnan(x_column)]
    y_column = y_column[~np.isnan(y_column)]
    # Fix the columns so they are the same length
    if len(x_column) > len(y_column):
        x_column = x_column[:len(y_column)]
    elif len(y_column) > len(x_column):
        y_column = y_column[:len(x_column)]

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_column, y_column)
    line = slope * x_column + intercept
    import plotly.graph_objects as go

    # Plot data points
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_column, y=y_column, mode="markers", name="Data Points"))
    fig.add_trace(go.Scatter(x=x_column, y=line, mode="lines", name="Regression Line", line = dict(color='firebrick', dash='dash')))

    fig.update_layout(
        title={
            "text": "Relationship between " + output_value + " and " + output_value2,
            "x": 0.1,
            "xanchor": "left",
        },
        xaxis_title=output_value,
        yaxis_title=output_value2,
        colorway=["#17B897"],
    )
    return fig

@callback(
    [Output("equation-relation", "children"),
    Output("correlation-relation", "children"),
    Output("pvalue-relation", "children"),
    Output("standard_error-relation", "children"),
    Output("intercept_stderr-relation", "children"),],
    [
        Input("input-filter", "value"),
        Input("output-filter", "value"),
        Input("output-filter2", "value"),
    ],
)
def set_equation(input_value, output_value, output_value2):
    df = pd.read_csv("datasets/" + input_value)
    x_column = df[output_value]
    y_column = df[output_value2]
    output_value = output_value.replace("_", " ").title()
    output_value2 = output_value2.replace("_", " ").title()
    df = pd.read_csv("datasets/" + input_value)
    
    # Plot line of best fit
    import scipy.stats as stats
    # remove nan values and the corresponding y values
    import numpy as np
    x_column = x_column[~np.isnan(x_column)]
    y_column = y_column[~np.isnan(y_column)]
    # Fix the columns so they are the same length
    if len(x_column) > len(y_column):
        x_column = x_column[:len(y_column)]
    elif len(y_column) > len(x_column):
        y_column = y_column[:len(x_column)]

    # result = stats.linregress(df[0], df[1])
    #     slope = result[0]
    #     intercept = result[1]
    #     r_value = result[2]
    #     p_value = result[3]
    #     std_err = result[4]
    #     intercept_err = 0
    #     import numpy as np
    #     intercept_stderr = std_err * np.sqrt(1/len(df[0]) + np.mean(df[0])**2/np.sum((df[0]-np.mean(df[0]))**2))
    #     equation = "y = " + str(round(slope, 2)) + "x + " + str(round(intercept, 2))
    #     correlation = "r = " + str(round(r_value, 2))
    #     pvalue = "P-value = " + str(round(p_value, 2))
    #     std_err = "Standard Error = " + str(round(std_err, 2))
    #     intercept_err = "Intercept Error = " + str(round(intercept_stderr, 2))
    #     return [html.Div(children=equation, className="menu-title-success"), 
    #             html.Div(children=correlation, className="menu-title-success"),
    #             html.Div(children=pvalue, className="menu-title-success"),
    #             html.Div(children=std_err, className="menu-title-success"),
    #             html.Div(children=intercept_err, className="menu-title-success")]
    result = stats.linregress(x_column, y_column)
    slope = result[0]
    intercept = result[1]
    r_value = result[2]
    p_value = result[3]
    std_err = result[4]
    intercept_err = 0
    import numpy as np
    intercept_stderr = std_err * np.sqrt(1/len(x_column) + np.mean(x_column)**2/np.sum((x_column-np.mean(x_column))**2))
    equation = "y = " + str(round(slope, 2)) + "x + " + str(round(intercept, 2))
    correlation = "r = " + str(round(r_value, 2))
    pvalue = "P-value = " + str(round(p_value, 2))
    std_err = "Standard Error = " + str(round(std_err, 2))
    intercept_err = "Intercept Error = " + str(round(intercept_stderr, 2))
    return [html.Div(children=equation, className="menu-title-success"),
            html.Div(children=correlation, className="menu-title-success"),
            html.Div(children=pvalue, className="menu-title-success"),
            html.Div(children=std_err, className="menu-title-success"),
            html.Div(children=intercept_err, className="menu-title-success")]


