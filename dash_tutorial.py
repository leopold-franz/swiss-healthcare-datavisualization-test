import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# The data comes from:
# https://www.bfs.admin.ch/bfs/en/home/statistics/catalogues-databases/tables.assetdetail.10767996.html
# I extracted some data from the 'je-d-14.04.01.02.04.xlsx' file into the 'data.csv' file
df = pd.read_csv('data.csv', index_col=0)

print(df.head())
print(list(df.columns))


# fig = px.line(df, x=df.index, y='2015')

app.layout = html.Div(children=[
    html.H1(children='Dash Demo'),

    html.Div(children='''
        Building a simple Dash app
    '''),

    html.Label('Year'),
    dcc.Dropdown(
        id='measurement_types-dropdown',
        options=[{'label': str(y), 'value': y} for y in df.columns],
        value=2015,
    ),

    html.Label(''),
    dcc.Graph(
        id='line_graph'
    )
])


@app.callback(
    Output('line_graph', 'figure'),
    [Input('measurement_types-dropdown', 'value')])
def update_figure(year):
    fig1 = px.line(df,
                   x=df.index,
                   y=df[str(year)],
                   title='Number of Hospitalized Patients in Switzerland '
                         'divided by Age Group in the year {}'.format(year),
                   labels={
                       "age_group": "Age Group",
                       str(year): "Number of Patients"
                   })
    return fig1


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8000, debug=True)
