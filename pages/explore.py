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
                        
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Enter y-axis Title", className="menu-title"),
                        dcc.Input(id="y-axis", type="text", placeholder="default: y-axis"),
                    ]
                ),

                # # Run button
                # html.Div(
                #     children=[
                #         html.Button(
                #             id="submit-button-state",
                #             n_clicks=0,
                #             children="Run Regression Analysis",
                #             className="button",
                #         ),
                #     ]
                # ),
                        
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
    Input("y-axis", "value"))
def update_chart(list_of_contents, list_of_names, list_of_dates, x_axis, y_axis):
    import plotly.graph_objs as go
    fig = go.Figure()
    fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "No matching data found. Please select a parameter or different date range.",
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
        print(x_axis)
        print(y_axis)
        if x_axis is None:
            x_axis = "x-axis"
        if y_axis is None:
            y_axis = "y-axis"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df[0], y=df[1], mode='lines', name='lines'))
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
