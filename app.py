import base64
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            html.Button('Upload File')
        ]),
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(dcc.Markdown('''
    You may upload a _.csv_ file containing data points. It should be formatted as follows:
    * Each $row$ contain the independent ($x$) and dependent ($y$) variable of a data point
    * The $1^{st} column$ contains the independent variable ($x$) of data points
    * The $2^{nd} column$ contains the dependent variable ($y$) of data points
    * The data set should be of size $n \\times 2$, where $n$ is the total number of data points''', mathjax=True)),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # returned value should be changed to a suitable data type as the input to the plotting function
    return html.Div([
        html.H6(filename),
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)
