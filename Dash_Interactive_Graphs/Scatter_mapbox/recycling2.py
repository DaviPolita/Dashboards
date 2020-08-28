import plotly.offline as py
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash
# import numpy as np
import pandas as pd
mapbox_access_token = "pk.eyJ1IjoiZGF2aXBvbGl0YSIsImEiOiJja2UxemU2M3AwNGFnMnptcTBsbjFmbHk1In0.rBKZJk5y0J5goUw6OdHRkw"

df = pd.read_csv("D:/Downloads/finalrecycling.csv")

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)

blackbold = {"color": "black", "font-weight": "bold"}

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Ul([
                html.Li("Component", className="circle", style={
                        "background": "#ff00ff", "color": "black", "list-style": "none", "text-indent": "17px"}),
                html.Li("Electronics", className="circle", style={
                        "background": "#0000ff", "color": "black", "list-style": "none", "text-indent": "17px"}),
                html.Li("Hazardous_waste", className="circle", style={
                        "background": "#ff0000", "color": "black", "list-style": "none", "text-indent": "17px"}),
                html.Li("Plastic_bags", className="circle", style={
                        "background": "#00ff00", "color": "black", "list-style": "none", "text-indent": "17px"}),
                html.Li("Recycling_bins", className="circle", style={
                        "background": "#824100", "color": "black", "list-style": "none", "text-indent": "17px"})
            ], style={"border-bottom": "solid 3px", "border-color": "#00fc87", "padding-top": "6px"}
            ),

            html.Label(children=["Borough: "], style=blackbold),
            dcc.Checklist(id="boro-name",
                          options=[{"label": str(i), "value": i}
                                   for i in sorted(df["boro"].unique())],
                          value=[i for i in sorted(df["boro"].unique())]
                          ),


            html.Label(children=["Looking to recycle: "], style=blackbold),
            dcc.Checklist(id="recycling-type",
                          options=[{"label": str(i), "value": i}
                                   for i in sorted(df["type"].unique())],
                          value=[i for i in sorted(df["type"].unique())]
                          ),


            html.Br(),
            html.Label(["Website:"], style=blackbold),
            html.Pre(id="web-link", children=[], style={'white-space': 'pre-wrap', 'word-break': 'break-all',
                                                        'border': '1px solid black', 'text-align': 'center',
                                                        'padding': '12px 12px 12px 12px', 'color': 'blue',
                                                        'margin-top': '3px'}
                     ),
        ], className="three columns"),


        html.Div([
            dcc.Graph(id="graph-id", config={"displayModeBar": False, "scrollZoom": True}, style={
                      'background': '#00FC87', 'padding-bottom': '2px', 'padding-left': '2px', 'height': '100vh'})

        ], className="nine columns"),

    ], className="row"),

], className="ten columns offset-by-one")


@app.callback(Output("graph-id", "figure"),
              [Input("boro-name", "value"),
               Input("recycling-type", "value")])
def update_figure(chosen_boro, chosen_recycling):
    dff = df[(df["boro"].isin(chosen_boro)) &
             (df["type"].isin(chosen_recycling))]

    location = [go.Scattermapbox(
        lon=dff["longitude"],
        lat=dff["latitude"],
        mode="markers",
        marker={"color": dff["color"]},
        unselected={"marker": {"opacity": 1}},
        selected={"marker": {"opacity": 0.5, "size": 25}},
        hoverinfo="text",
        hovertext=dff["hov_txt"],
        customdata=dff["website"]
    )]

    return {
        "data": location,
        "layout": go.Layout(
            uirevision="foo",
            clickmode="event+select",
            hovermode="closest",
            hoverdistance=2,
            title=dict(text="Where to Recycle My Stuff?",
                       font=dict(size=50, color="red")),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style="light",
                center=dict(
                    lat=40.80105,
                    lon=-73.945155),
                pitch=40,
                zoom=11.5
            )
        )
    }


@app.callback(
    Output("web-link", "children"),
    [Input("graph-id", "clickData")])
def display_click_data(clickData):
    if clickData is None:
        return "Click on any point"
    else:
        print(clickData)
        the_link = clickData["points"][0]["customdata"]
        if the_link is None:
            return "No website available"
        else:
            return html.A(the_link, href=the_link, target="_blank")


if __name__ == "__main__":
    app.run_server(debug=True)
