import dash
from dash import html, dcc, callback, Input, Output, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime
import plotly.express as px
import base64
import io
from sklearn.metrics import mean_squared_error
import scipy.stats as stats
import numpy as np
import plotly.graph_objs as go
import json

layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Explore your own dataset", className="header-title"
                ),
                html.P(
                    children="You may upload a .csv file containing data points. It should be formatted as follows:",
                    className="header-description",
                ),
                html.Div(dcc.Markdown('''
                * Each $row$ contain the independent ($x$) and dependent ($y$) variable of a data point
                * The $1^{st} column$ contains the independent variable ($x$) of data points
                * The $2^{nd} column$ contains the dependent variable ($y$) of data points
                * The data set should be of size $n \\times 2$, where $n$ is the total number of data points''', mathjax=True),className="header-description",),
                # Split the above div up into 4 P blocks
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Upload .csv file", className="menu-title"),
                        # Make an upload button
                        dcc.Upload(id='upload-data',
                        multiple=True,
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select a File')
                            
                        ], style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center'
                        })),

                    html.Div(id="warning", className="menu-title"),
                    ]
                ),
                html.Div(
                    children=[

                        # Indicate what the x and y axis are
                        html.Div(children="Enter x-axis Title", className="menu-title"),
                        dcc.Input(id="x-axis", type="text", placeholder="default: x-axis", className="select"),
                        html.Div(children="Enter y-axis Title", className="menu-title"),
                        dcc.Input(id="y-axis", type="text", placeholder="default: y-axis"),
                        
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Enter custom slope", className="menu-title"),
                        dcc.Input(id="slope", type="text", placeholder="default: 1", className="select", ),
                        html.Div(children="Enter custom intercept", className="menu-title"),
                        dcc.Input(id="intercept", type="text", placeholder="default: 0"),
                    ]
                ),
                        
            ],
            className="menu-explore",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="explore-chart",
                        config={"displayModeBar": True},
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
                html.Pre(id='relayout-data', children=""),
                dcc.Store(id='plot-data'),
                dcc.Store(id='file-name')
            ]
        ),
        html.Div(
            children=[
                # Display the data from the graph
                # such as the equation of the line
                # and the correlation coefficien
                html.Div(
                    children=[
                        html.Div(children="Equation of the line", className="menu-title"),
                        html.Div(id="equation", className="warning"),
                    ], 
                ),
                # Pearson correlation coefficient
                html.Div(
                    children=[
                        html.Div(children="Pearson correlation coefficient", className="menu-title"),
                        html.Div(id="correlation", className="warning"),
                    ], 
                ),
                # pvalue
                html.Div(
                    children=[
                        html.Div(children="P-value", className="menu-title"),
                        html.Div(id="pvalue", className="warning"),
                    ], 
                ),
                # Standard error of the estimated slope
                html.Div(
                    children=[
                        html.Div(children="Standard error of the estimated slope", className="menu-title"),
                        html.Div(id="standard_error", className="warning"),
                    ], 
                ),
                # intercept_stderr
                html.Div(
                    children=[
                        html.Div(children="Standard error of the estimated intercept", className="menu-title"),
                        html.Div(id="intercept_stderr", className="warning"),          
                    ], 
                ),
                # Estimate RMSE
                html.Div(
                    children=[
                        html.Div(children="Root-mean-squared error for estimate", className="menu-title"),
                        html.Div(id="estimate_rmse", className="warning"),
                    ], 
                ),
               # Custom function RMSE
                html.Div(
                    children=[
                        html.Div(children="Root-mean-squared error for input", className="menu-title"),
                        html.Div(id="input_rmse", className="warning"),
                    ], 
                )
            ], style={'height': '100%', 'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-evenly'},
            className="menu-explore-data",
        ),
        
        ]

)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.DataFrame()
    x_axis = ""
    y_axis = ""
    print(filename)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            # Check if first row is a header
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
            print(df, flush=True)
    except Exception as e:
        pass
    return df
    
@callback(Output('warning', 'children'),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified'),)
def update_output(list_of_contents, list_of_names, list_of_dates):
    children = []
    if list_of_contents is not None:
        print("Calling parse_contents over children", flush=True)
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
    if len(children) == 0:
        return html.Div(children="No file has been uploaded yet", className="menu-title-warning")
    elif children[0].shape[1] != 2:
        print("Bruh", flush=True)
        return html.Div(children="Invalid file format. Please upload a .csv file", className="menu-title-warning")
    else:
        return html.Div(children="File uploaded successfully", className="menu-title-success")

@callback(
    Output("relayout-data", "children"),
    Output("plot-data", "data"),
    Output("file-name", "data"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    State("plot-data", "data"),
    State("file-name", "data"),
    Input("explore-chart", "relayoutData"),
)
def read_file(list_of_contents, list_of_names, list_of_dates, last_plot_data, last_file_name, relayoutData):
    relayoutText = json.dumps(relayoutData, indent=2)

    if list_of_names and list_of_names[0] == last_file_name:
        df = last_plot_data
    else:
        children = []
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
        
        if len(children) == 0:
            print("No children")
            return [relayoutText, None, last_file_name]
        elif children[0].shape[1] != 2:
            print("Shape wrong")
            return [relayoutText, None, last_file_name]
        else:
            # relayoutData.shapes
            df = children[0]
            last_file_name = list_of_names[0]

    if "shapes" in relayoutData:
        print("Drew line")
        line = relayoutData["shapes"][0]
        return [relayoutText, [list(df[0]) + [line["x0"]], list(df[1]) + [line["y0"]]], last_file_name]
    else:
        print("Oops")
        return [relayoutText, [df[0], df[1]], last_file_name]

@callback(
    [Output("explore-chart", "figure"),
    Output('input_rmse', 'children')],
    Input("plot-data", "data"),
    Input("x-axis", "value"),
    Input("y-axis", "value"),
    Input("slope", "value"),
    Input("intercept", "value"))
def update_chart(df, x_axis, y_axis, slope, intercept):
    fig = go.Figure()
    fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "No matching data found. Please upload a file or make sure the file is formatted correctly.",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
    if df is None:
        return [fig, html.Div(children=0, className="menu-title-success")]
    else:
        print("test")
        print(df)
        df = pd.concat([pd.Series(df[0]), pd.Series(df[1])], axis=1)
        print(df)
        # Get the linear regression line
        slopeInput = slope
        interceptInput = intercept
        slope, intercept, _, _, _ = stats.linregress(df[0], df[1])

        # Plot a line with the input slope and intercept
        if x_axis is None:
            x_axis = "x-axis"
        if y_axis is None:
            y_axis = "y-axis"
        if slopeInput is None or len(slopeInput) == 0:
            slopeInput = 1
        if interceptInput is None or len(interceptInput) == 0:
            interceptInput = 0

        slopeInput = float(slopeInput)
        interceptInput = float(interceptInput)

        y_predicted_input = slopeInput * df[0] + interceptInput
        rmse_input = mean_squared_error(df[1], y_predicted_input, squared=False)

        # Plot a line with the input slope and intercept
        fig = go.Figure()
        # Add scatter plot of data
        fig.add_trace(go.Scatter(x=df[0], y=df[1], mode='markers', name='data'))
        fig.add_trace(go.Scatter(x=df[0], y=slope*df[0]+intercept, mode='lines', name='regression line'))
        fig.add_trace(go.Scatter(x=df[0], y=slopeInput*df[0]+interceptInput, mode='lines', name='input line', line = dict(color='firebrick', dash='dash')))
        # fig.add_vrect(
        #     x0=-100, x1=100,
        #     fillcolor="LightSalmon", opacity=0,
        #     layer="below", line_width=0,
        # )
        # fig.add_shape(type="rect",
        #     xref="paper", yref="paper",
        #     x0=0, x1=1, y0=0, y1=1,
        #     line_width=0
        # )
        fig.layout.shapes
        fig.update_layout(
            title={
                "text": "Relationship between " + x_axis + " and " + y_axis,
                "x": 0.1,
                "xanchor": "left",
            },
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            colorway=["#17B897"],
            dragmode='drawline'
        )
        return [
            fig,
            html.Div(children=rmse_input, className="menu-title-success")
        ]

@callback(
    [Output("equation", "children"),
    Output("correlation", "children"),
    Output("pvalue", "children"),
    Output("standard_error", "children"),
    Output("intercept_stderr", "children"),
    Output('estimate_rmse', 'children')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'))
def update_equation(list_of_contents, list_of_names, list_of_dates):
    children = []
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
    if len(children) == 0:
        return ["" for _ in range(6)]
    elif children[0].shape[1] != 2:
        return ["" for _ in range(6)]
    else:
        df = children[0]
        # Get the linear regression line
        result = stats.linregress(df[0], df[1])
        slope, intercept, r_value, p_value, std_err = result
        intercept_err = 0

        y_predicted_estimate = slope * df[0] + intercept
        rmse = mean_squared_error(df[1], y_predicted_estimate, squared=False)

        intercept_stderr = std_err * np.sqrt(1/len(df[0]) + np.mean(df[0])**2/np.sum((df[0]-np.mean(df[0]))**2))
        equation = "y = " + str(round(slope, 2)) + "x + " + str(round(intercept, 2))
        correlation = "r = " + str(round(r_value, 2))
        pvalue = "P-value = " + str(round(p_value, 2))
        std_err = "Standard Error = " + str(round(std_err, 2))
        intercept_err = "Intercept Error = " + str(round(intercept_stderr, 2))
        return [html.Div(children=equation, className="menu-title-success"), 
                html.Div(children=correlation, className="menu-title-success"),
                html.Div(children=pvalue, className="menu-title-success"),
                html.Div(children=std_err, className="menu-title-success"),
                html.Div(children=intercept_err, className="menu-title-success"),
                html.Div(children=rmse, className="menu-title-success")]
    