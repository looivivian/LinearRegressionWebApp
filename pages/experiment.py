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
import math

layout = html.Div(
    children=[
        html.Div(
            children=[
                # insert image 
               
                html.H1(
                    children="Experiment with gradient descent parameters", className="header-title"
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
                        dcc.Upload(id='upload-data-gd',
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
                            'textAlign': 'center',
                        })),

                    html.Div(id="warning-gd", className="menu-title"),
                    ], style={
                    'padding-right': '25px',
                    'padding-left': '25px'}
                ),
                html.Div(
                    children=[

                        # Indicate what the x and y axis are
                        html.Div(children="Enter x-axis Title", className="menu-title"),
                        dcc.Input(id="x-axis-gd", type="text", placeholder="default: x-axis", className="select"),
                        html.Div(children="Enter y-axis Title", className="menu-title"),
                        dcc.Input(id="y-axis-gd", type="text", placeholder="default: y-axis"),
                        
                    ], style={
                    'padding-right': '25px',
                    'padding-left': '25px'}
                ),
                html.Div(
                    children=[
                        html.Div(children="Enter learning rate", className="menu-title"),
                        dcc.Input(id="learning_rate", type="text", placeholder="default: 0.001", className="select", ),
                        html.Div(children="Enter number of epochs", className="menu-title"),
                        dcc.Input(id="num_epochs", type="text", placeholder="default: 1000"),
                    ], style={
                    'padding-right': '25px',
                    'padding-left': '25px'}
                ),
                html.Div(
                    children=[
                        html.Div(children="Enter initial weight", className="menu-title"),
                        dcc.Input(id="init_w", type="text", placeholder="default: 0"),
                        html.Div(children="Enter initial bias", className="menu-title"),
                        dcc.Input(id="init_b", type="text", placeholder="default: 0"),
                    ], style={
                    'padding-right': '25px',
                    'padding-left': '25px'}
                )
                        
            ],
            className="menu-explore",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="explore-chart-gd",
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
                        html.Div(children="Weight", className="menu-title"),
                        html.Div(id="weight", className="warning"),
                    ], 
                ),
                # Pearson correlation coefficient
                html.Div(
                    children=[
                        html.Div(children="Bias", className="menu-title"),
                        html.Div(id="bias", className="warning"),
                    ], 
                ),
                # pvalue
                html.Div(
                    children=[
                        html.Div(children="Final Cost", className="menu-title"),
                        html.Div(id="cost", className="warning"),
                    ], 
                ),
            ], style={'height': '100%', 'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-evenly'},
            className="menu-explore-data",
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="cost-chart-gd",
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
                                    "text": "Cost over epochs",
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
        )
        ]
)

"""
 Parse the contents of a file and return a dataframe.
 
 @param contents - The contents of the file.
 @param filename - The filename of the file to parse
 @param date - The date of the file to parse
"""
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
    


"""
 Callback function to update the output of the file and store state of the file contents.
 
 @param list_of_contents - list of contents of the file
 @param list_of_names - list of names of files to be uploaded
 @param list_of_dates - list of dates of files.
"""
@callback(Output('warning-gd', 'children'),
            Input('upload-data-gd', 'contents'),
            State('upload-data-gd', 'filename'),
            State('upload-data-gd', 'last_modified'),)
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
        
"""
 This function is called when the chart is updated.
 
 @param list_of_contents - list of contents of the chart.
 @param list_of_names - list of contents of the chart.
 @param list_of_dates - list of contents of the chart.
 @param x_axis - The x axis of the chart.
 @param y_axis - The y axis of the chart.
 @param learning_rate - learning rate of the learning rate of the chart.
 @param num_epochs - learning rate of the chart.
 @param init_w - initial weight and bias values
 @param init_b - initial weight weight and bias
"""
@callback(
    [Output("explore-chart-gd", "figure"),
    Output("cost-chart-gd", "figure"),
    Output('cost', 'children'),
    Output('weight', 'children'),
    Output('bias', 'children')],
    Input('upload-data-gd', 'contents'),
    State('upload-data-gd', 'filename'),
    State('upload-data-gd', 'last_modified'),
    Input("x-axis-gd", "value"),
    Input("y-axis-gd", "value"),
    Input("learning_rate", "value"),
    Input("num_epochs", "value"),
    Input("init_w", "value"),
    Input("init_b", "value"))
def update_chart(list_of_contents, list_of_names, list_of_dates, x_axis, y_axis, learning_rate, num_epochs, init_w, init_b):
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
        return [
            fig,
            go.Figure(),
            html.Div(children=0, className="menu-title-success"), 
            html.Div(children=0, className="menu-title-success"), 
            html.Div(children=0, className="menu-title-success")]
    elif children[0].shape[1] != 2:
        return [
            fig, 
            go.Figure(),
            html.Div(children=0, className="menu-title-success"),
            html.Div(children=0, className="menu-title-success"),
            html.Div(children=0, className="menu-title-success")]
    else:
        df = children[0]

        if not init_b:
            init_b = 0
        
        if not init_w:
            init_w = 0

        if not learning_rate:
            learning_rate = 0.001
        
        if not num_epochs:
            num_epochs = 1000

        init_b = float(init_b)
        init_w = float(init_w)
        learning_rate = float(learning_rate)
        num_epochs = int(num_epochs)

        w, b, J_history, p_history = run_gradient_descent(df[0], df[1], init_w, init_b, learning_rate, num_epochs)

        if x_axis is None:
            x_axis = "x-axis"
        if y_axis is None:
            y_axis = "y-axis"

        print(w, b)

        fig = go.Figure()
        # Add scatter plot of data
        fig.add_trace(go.Scatter(x=df[0], y=df[1], mode='markers', name='data'))
        fig.add_trace(go.Scatter(x=df[0], y=w*df[0]+b, mode='lines', name='regression line'))
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

        cost_fig = go.Figure()
        cost_fig.add_trace(go.Scatter(x0=1, y=J_history, mode='lines', name='Cost'))
        cost_fig.update_layout(
            title= {
                "text": "Cost over epochs",
                "x": 0.1,
                "xanchor": "left",
            },
            xaxis= {"fixedrange": True},
            yaxis= {
                "fixedrange": True,
            },
            xaxis_title="Epochs",
            yaxis_title="Cost",
            colorway= ["#17B897"],
        )


        return [
            fig,
            cost_fig,
            html.Div(children=J_history[-1], className="menu-title-success"),
            html.Div(children=w, className="menu-title-success"),
            html.Div(children=b, className="menu-title-success")
        ]
    
# NOTE: Most of the code below is adapted from the starter code provided in Quiz 6

def f_wb(x, w, b):
    """
    Computes the prediction of a linear model
    Args:
      x (scalar): input value 
      w,b (scalar): model parameters  
    Returns
      predicted value based on x, w, and b
    """
    return w * x + b

def compute_cost(x, y, w, b):
    """
    Computes the cost of a model
    Args:
      x (ndarray(m,)): input values, m examples
      y (ndarray(m,)): output values, m examples (the correct answers)
      w,b (scalar): model parameters  
    Returns
      cost based on mean square error of prediction (using x, w, and b) and the correct asnwer (y)
    """
    m = x.shape[0] 
    cost = 0
    
    for i in range(m):
        cost = cost + (f_wb(x[i], w, b) - y[i])**2
    total_cost = 1 / (2 * m) * cost

    return total_cost

def compute_gradient(x, y, w, b): 
    """
    Computes the gradient for linear regression 
    Args:
      x (ndarray (m,)): input values, m examples
      y (ndarray (m,)): output values, m examples (the correct answers)
      w,b (scalar)    : model parameters  
    Returns
      dj_dw (scalar): The gradient of the cost w.r.t. the parameters w
      dj_db (scalar): The gradient of the cost w.r.t. the parameter b     
     """
    
    # Number of training examples
    m = x.shape[0]    
    dj_dw = 0
    dj_db = 0
    
    for i in range(m):  
        dj_dw += (f_wb(x[i], w, b) - y[i]) * x[i]
        dj_db += (f_wb(x[i], w, b) - y[i])
    dj_dw = dj_dw / m
    dj_db = dj_db / m
        
    return dj_dw, dj_db

def run_gradient_descent(x_train, y_train, w_initial, b_initial, alpha, num_iters):
    """
    Runs gradient descent to learn the parameters of a linear model
    Args:
        x_train (ndarray (m,)): input values, m examples
        y_train (ndarray (m,)): output values, m examples (the correct answers)
        w_initial (scalar): initial value of the parameter w
        b_initial (scalar): initial value of the parameter b
        alpha (scalar): learning rate
        num_iters (int): number of iterations to run gradient descent
    Returns:
        w (scalar): the learned value of the parameter w
        b (scalar): the learned value of the parameter b
        J_history (ndarray (num_iters,)): the cost at each iteration
        p_history (ndarray (num_iters, 2)): the parameters at each iteration
    """
    w = w_initial
    b = b_initial
    
    J_history, p_history = [], []

    for i in range(num_iters):
        
        # Get the gradients
        dj_dw, dj_db = compute_gradient(x_train, y_train, w, b)
    
        # Update parameters
        w = w - alpha * dj_dw                       
        b = b - alpha * dj_db

        # Save off for plotting
        J_history.append(compute_cost(x_train, y_train, w , b))
        p_history.append([w,b])
    
        # Print cost every at intervals
        if i% math.ceil(num_iters/10) == 0:
            print(f"Iteration {i:4}: Cost {J_history[-1]:0.2e} ",
                  f"dj_dw: {dj_dw: 0.3e}, dj_db: {dj_db: 0.3e}  ",
                  f"w: {w: 0.3e}, b:{b: 0.5e}")
            
    return w, b, J_history, p_history