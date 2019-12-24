# -*- coding: utf-8 -*-

# Author: Matteo Esposito
# December 2019

import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

app = dash.Dash("Dash Project", external_stylesheets=[
                'https://codepen.io/amyoshino/pen/jzXypZ.css'])
app.title = "GD Visualizer"

# Read in grades data.
df = pd.read_csv("distributions.csv", low_memory=True)

# Define letter to grade mapping
LETTERS = {'A+':4.3, 'A':4, 'A-':3.7, 'B+':3.3, 'B':3, 'B-':2.7, 'C+':2.3,
           'C':2, 'C-':1.7, 'D+':1.3, 'D':1, 'D-':0.7, 'F':0, 'FNS':0, 'R':0, 'NR':0}

# Populate years and grades.
grades = {}
all_options = df.groupby('Year')['Class'].apply(lambda x: x.tolist()).to_dict()
all_years = df['Year'].unique()
for cl in df['Class']:
    grades[cl] = {"x": list(LETTERS.keys()), "y": df[df.Class==cl][LETTERS].values.tolist()[0]}

app.layout = html.Div(
    html.Div([

        # Title/Header
        html.Div([
            html.H3('Grade Distribution Visualizer', className="nine columns"),
        ], className="row"),

        # Selectors
        html.Div([
            html.Div([
                html.P('Choose Class:'),
                dcc.Checklist(
                    id='course-selector',
                    value=['ACTU 256'],
                    labelStyle={'display': 'inline-block'}
                ),
            ], className='six columns', style={'margin-top': '10'}),
            html.Div([
                html.P('Choose Year:'),
                dcc.Dropdown(
                    id='year-selector',
                    options=[{'label': i, 'value': i} for i in all_years],
                    value=2016
                ),
            ], className='six columns', style={'margin-bottom': '10'})
        ], className="row"),

        html.Div([
            # Graph
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
                                    family='Roboto, monospace',
                                    size=17,
                                    color='#7f7f7f'
                                )
                            ),
                            'yaxis': dict(
                                title='Frequency',
                                titlefont=dict(
                                    family='Roboto, monospace',
                                    size=17,
                                    color='#7f7f7f'
                                )
                            )
                        }
                    },
                    style={"border":"1px black solid", 'padding':15}
                )
            ], className="six columns"),
            # Table
            html.Div([
                dt.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    # fixed_columns={'headers': True, 'data': 3},
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'Region'},
                            'textAlign': 'left'
                        }
                    ],
                    style_table={'overflowX': 'scroll'},
                )
            ], className="six columns")
        ], className="row"),

        # Title/Header
        html.Div([
            html.Footer(
                "Made by Matteo Esposito, 2019", 
                style={  
                    'position': 'absolute',
                    'right': 0,
                    'bottom': 0,
                    'left': 0,
                    'padding': 5,
                    'background-color': '#efefef',
                    # 'font-family': 'Roboto, monospace',
                    'text-align': 'center'})
        ], className="row"),
    ])
)



# Update list of available courses.
@app.callback(
    dash.dependencies.Output('course-selector', 'options'),
    [dash.dependencies.Input('year-selector', 'value')])
def set_course_options(selected_year):
    return [{'label': i, 'value': i} for i in list(all_options[selected_year])]

# Update dataframe view.
@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('year-selector', 'value')])
def update_table(selected_year):
    newtab = df.copy()
    newtab = newtab[newtab['Year'] == selected_year]
    data = newtab.to_dict('records')
    return data

# Update graph.
@app.callback(
    dash.dependencies.Output('distribution-graph', 'figure'),
    [dash.dependencies.Input('course-selector', 'value')])
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
                    family='Roboto, monospace',
                    size=14,
                    color='#7f7f7f'
                )),
            'yaxis': dict(
                title='Frequency',
                titlefont=dict(
                    family='Roboto, monospace',
                    size=14,
                    color='#7f7f7f'
                ))
        }
    }
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
