import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly
import plotly.express as px

import pandas as pd

df = pd.read_csv(
    "C:/Projetos_C/Dash/Tutorial/Dash-by-Plotly-master/Dash_Interactive_Graphs/suicide_rates.csv")

mark_values = {1985: '1985', 1988: '1988', 1991: '1991', 1994: '1994',
               1997: '1997', 2000: '2000', 2003: '2003', 2006: '2006',
               2009: '2009', 2012: '2012', 2015: '2015', 2016: '2016'}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Pre(children="Suicide Rates 1985-2016",
                 style={"text-align": "center", "font-size": "100%", "color": "black"})
    ]),

    html.Div([
        dcc.Graph(id="the-graph")
    ]),

    html.Div([
        dcc.RangeSlider(id="the-year",
                        min=1985,
                        max=2016,
                        value=[1985, 1988],
                        marks=mark_values,
                        step=None)
    ], style={"width": "70%", "position": "absolute", "left": "5%"})

])


@app.callback(
    Output("the-graph", "figure"),
    [Input("the-year", "value")]
)
def update_graph(years_chosen):

    dff = df[(df["year"] >= years_chosen[0]) &
             (df["year"] <= years_chosen[1])]

    dff = dff.groupby(["country"], as_index=False)[
        "suicides/100k pop", "gdp_per_capita ($)"].mean()

    scatterplot = px.scatter(
        data_frame=dff,
        x="suicides/100k pop",
        y="gdp_per_capita ($)",
        hover_data=["country"],
        text="country",
        height=550

    )

    scatterplot.update_traces(textposition="top center")

    return (scatterplot)


if __name__ == "__main__":
    app.run_server(debug=True)
