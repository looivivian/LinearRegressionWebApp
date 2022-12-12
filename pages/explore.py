import dash
from dash import html, dcc, callback, Input, Output, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import datetime
import plotly.express as px
import base64
import io

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
                        html.Div(id="equation", className="warning"),
                    ]
                ),
                # Pearson correlation coefficient
                html.Div(
                    children=[
                        html.Div(children="Pearson correlation coefficient", className="menu-title"),
                        html.Div(id="correlation", className="warning"),
                        
                    ]
                ),
                # pvalue
                html.Div(
                    children=[
                        html.Div(children="P-value", className="menu-title"),
                        html.Div(id="pvalue", className="warning"),
                        
                    ]
                ),
                # Standard error of the estimated slope
                html.Div(
                    children=[
                        html.Div(children="Standard error of the estimated slope", className="menu-title"),
                        html.Div(id="standard_error", className="warning"),
                        
                    ]
                ),
                # intercept_stderr
                html.Div(
                    children=[
                        html.Div(children="Standard error of the estimated intercept", className="menu-title"),
                        html.Div(id="intercept_stderr", className="warning"),
                        
                    ]
                ),



            ],
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
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            # Check if first row is a header
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
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
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
    if len(children) == 0:
        return html.Div(children="No file has been uploaded yet", className="menu-title-warning")
    elif children[0].shape[1] != 2:
        return html.Div(children="Invalid file format. Please upload a .csv file", className="menu-title-warning")
    else:
        return html.Div(children="File uploaded successfully", className="menu-title-success")
        

@callback(
    Output("explore-chart", "figure"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    Input("x-axis", "value"),
    Input("y-axis", "value"),
    Input("slope", "value"),
    Input("intercept", "value"))
def update_chart(list_of_contents, list_of_names, list_of_dates, x_axis, y_axis, slope, intercept):
    import plotly.graph_objs as go
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
    children = []
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
    
    if len(children) == 0:
        return fig
    elif children[0].shape[1] != 2:
        return fig
    else:
        df = children[0]
        # Get the linear regression line
        import scipy.stats as stats
        slopeInput = slope
        interceptInput = intercept
        slope, intercept, r_value, p_value, std_err = stats.linregress(df[0], df[1])
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
        # Plot a line with the input slope and intercept
        fig = go.Figure()
        # Add scatter plot of data
        fig.add_trace(go.Scatter(x=df[0], y=df[1], mode='markers', name='data'))
        fig.add_trace(go.Scatter(x=df[0], y=slope*df[0]+intercept, mode='lines', name='regression line'))
        fig.add_trace(go.Scatter(x=df[0], y=slopeInput*df[0]+interceptInput, mode='lines', name='input line', line = dict(color='firebrick', dash='dash')))
        fig.update_layout(
            title={
                "text": "Relationship between " + x_axis + " and " + y_axis,
                "x": 0.1,
                "xanchor": "left",
            },
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            colorway=["#17B897"],
        )
        return fig

@callback(
    [Output("equation", "children"),
    Output("correlation", "children"),
    Output("pvalue", "children"),
    Output("standard_error", "children"),
    Output("intercept_stderr", "children"),],
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
        return "","","","",""
    elif children[0].shape[1] != 2:
        return "","","","",""
    else:
        df = children[0]
        # Get the linear regression line
        import scipy.stats as stats
        result = stats.linregress(df[0], df[1])
        slope = result[0]
        intercept = result[1]
        r_value = result[2]
        p_value = result[3]
        std_err = result[4]
        intercept_err = 0
        import numpy as np
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
                html.Div(children=intercept_err, className="menu-title-success")]
