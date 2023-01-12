import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# The data comes from:
# https://www.bfs.admin.ch/bfs/en/home/statistics/catalogues-databases/tables.assetdetail.10767996.html
# I extracted some data from the 'je-d-14.04.01.02.04.xlsx' file into the 'data.csv' file
print(Path.cwd())
df = pd.read_csv('data/data.csv', index_col=0)

print(df.head())
print(list(df.columns))

# 3. b) The plotly express line graph built using data
static_fig = px.line(df, x=df.index, y='2015')

app.layout = html.Div(children=[
    html.H1(children='Dash Demo'),

    # 1. Simplest Dash App
    html.Div(children="Building a simple Dash app. Hello World of Dash Apps! "
                      "Have a look at the code of this app and unblock more features by uncommenting code blocks!"),

    # 2. Adding a Dash Component to our App
    html.Label('Year'),
    dcc.Dropdown(
        id='measurement_types-dropdown',
        options=[{'label': str(y), 'value': y} for y in df.columns],
        value=2015,
    ),

    # 3. a) Adding a static graph
    # dcc.Graph(id='line_graph-1', figure=static_fig),

    # Recomment Part 3
    # 4. a) Adding a graph dependent of a dash callback
    html.Label('Plotly Graph'),

    # Recomment Part 4.a)
    # 5. Adding a loading icon to graph while it loads
    dcc.Loading(children=[dcc.Graph(id='line_graph')]),

])


# 4. b) The corresponding callback function that makes use of python function decorators
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
    app.run_server(host='0.0.0.0', port=80, debug=True)
