import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)


# import data and clean it
df = pd.read_csv(
    "D:/Downloads/DOHMH_New_York_City_Restaurant_Inspection_Results.csv")
df["INSPECTION DATE"] = pd.to_datetime(df["INSPECTION DATE"])
df = df.groupby(["INSPECTION DATE", "CUISINE DESCRIPTION",
                 "CAMIS"], as_index=False)["SCORE"].mean()
df = df.set_index("INSPECTION DATE")
df = df.loc["2016-01-01": "2019-12-31"]
df = df.groupby([pd.Grouper(freq="M"), "CUISINE DESCRIPTION"])[
    "SCORE"].mean().reset_index()

app.layout = html.Div([

    html.Div([
        dcc.Graph(id="our_graph")
    ], className="nine columns"),

    html.Div([

        html.Br(),

        html.Label(["Choose 3 Cuisines to Compare:"], style={
                   "font-weight": "bold", "text-align": "center"}),

        dcc.Dropdown(id='cuisine_one',
                     options=[{"label": x, "value": x} for x in df.sort_values(
                         "CUISINE DESCRIPTION")["CUISINE DESCRIPTION"].unique()],
                     value='African',
                     multi=False,
                     disabled=False,
                     clearable=True,
                     searchable=True,
                     placeholder='Choose Cuisine...',
                     className='form-dropdown',
                     style={'width': "90%"},
                     persistence='string',
                     persistence_type='memory'),

        dcc.Dropdown(id='cuisine_two',
                     options=[{'label': x, 'value': x} for x in df.sort_values(
                         'CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
                     value='Asian',
                     multi=False,
                     clearable=False,
                     persistence='string',
                     persistence_type='session'),

        dcc.Dropdown(id='cuisine_three',
                     options=[{'label': x, 'value': x} for x in df.sort_values(
                         'CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
                     value='Donuts',
                     multi=False,
                     clearable=False,
                     persistence='string',
                     persistence_type='local'),
    ], className="three columns"),
])


@app.callback(
    Output("our_graph", "figure"),
    [Input("cuisine_one", "value"),
     Input("cuisine_two", "value"),
     Input("cuisine_three", "value")]
)
def build_graph(first_cuisine, second_cuisine, third_cuisine):
    dff = df[
        (df["CUISINE DESCRIPTION"] == first_cuisine) |
        (df["CUISINE DESCRIPTION"] == second_cuisine) |
        (df["CUISINE DESCRIPTION"] == third_cuisine)]

    fig = px.line(dff, x="INSPECTION DATE", y="SCORE",
                  color="CUISINE DESCRIPTION", height=600)
    fig.update_layout(xaxis={"title": "NEGATIVE POINT"},
                      title={"text": "Restaurant Inspections in NYC", "font": {"size": 28}, "x": 0.5, "xanchor": "center"})

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
