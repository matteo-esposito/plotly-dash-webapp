# -*- coding: utf-8 -*-

# Author: Matteo Esposito
# December 2019

import pandas as pd
import dash._utils
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash("Dash Project", external_stylesheets=[
                'https://codepen.io/amyoshino/pen/jzXypZ.css'])
app.title = "Matteo | Dash"

all_options = {
    '2016': ['ACTU 256', 'INTE 293', 'MATH 251', 'MATH 264', 'STAT 249'],
    '2017': [],
    '2018': [],
    '2019': [],
    '2020': []
}

grades = {
    'ACTU 256': {'x': ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'FNS', 'R', 'NR'], 'y': [11, 10, 14, 7, 18, 5, 3, 3, 5, 0, 1, 1, 0, 2, 0, 0]}
}

app.layout = html.Div(
    html.Div([

        # Title/Header
        html.Div([
            html.H1('Grade Distribution Visualizer', className="nine columns"),
            html.Div('Concordia University Grade Distribution Visualizer (Fall 2016 to Winter 2020)',
                     className="nine columns")
        ], className="row"),

        # Selectors
        html.Div([
            html.Div([
                html.P('Choose Class:'),
                dcc.Checklist(
                    id='Courses',
                    value=[],
                    labelStyle={'display': 'inline-block'}
                ),
            ], className='six columns', style={'margin-top': '10'}),
            html.Div([
                html.P('Choose Year:'),
                dcc.RadioItems(
                    id='Years',
                    options=[{'label': k, 'value': k}
                             for k in all_options.keys()],
                    value='2016',
                    labelStyle={'display': 'inline-block'}
                ),
            ], className='six columns', style={'margin-top': '10'})
        ], className="row"),

        # Graphs
        html.Div([
            html.Div([
                dcc.Graph(
                    id='distribution-graph',
                    figure={
                        'data': [],
                        'layout': {
                            'title': 'Dash Data Viz',
                            'xaxis': dict(
                                title='Grades',
                                titlefont=dict(
                                    family='Monaco, monospace',
                                    size=17,
                                    color='#7f7f7f'
                                )),
                            'yaxis': dict(
                                title='Frequency',
                                titlefont=dict(
                                    family='Monaco, monospace',
                                    size=17,
                                    color='#7f7f7f'
                                ))
                        }
                    }
                )
            ], className="six columns"),
        ], className="row")
    ])
)


@app.callback(
    dash.dependencies.Output('Courses', 'options'),
    [dash.dependencies.Input('Years', 'value')])
def set_cities_options(selected_year):
    return [{'label': i, 'value': i} for i in all_options[selected_year]]


@app.callback(
    dash.dependencies.Output('distribution-graph', 'figure'),
    [dash.dependencies.Input('Courses', 'value')])
def update_graph_src(selector):
    data = []
    for course in selector:
        data.append({'x': grades[course]['x'], 'y': grades[course]['y'],
                     'type': 'bar', 'name': course})
    figure = {
        'data': data,
        'layout': {
            'title': 'Distribution Graph',
            'xaxis': dict(
                title='Grade',
                titlefont=dict(
                    family='Monaco, monospace',
                    size=20,
                    color='#7f7f7f'
                )),
            'yaxis': dict(
                title='Frequency',
                titlefont=dict(
                    family='Monaco, monospace',
                    size=20,
                    color='#7f7f7f'
                ))
        }
    }
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
