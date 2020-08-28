
import threading
from dash_html_components.Option import Option
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)


# limpa os dados

df = pd.read_csv("intro_bees.csv")

df = df.groupby(["State", "ANSI", "Affected by", "Year", "state_code"])[
    ["Pct of Colonies Impacted"]].mean()
df.reset_index(inplace=True)
# print(df.head())

# layout

# app.layout = html.Div([
#     html.H1("Web Application Dashboards with Dash",
#             style={"text-align": "center"}),

#     dcc.Dropdown(id="slct_cause",
#                  options=[
#                     {"label": "2015", "value": 2015},
#                     {"label": "2016", "value": 2016},
#                     {"label": "2017", "value": 2017},
#                     {"label": "2018", "value": 2018}],
#                  multi=False,
#                  value=2015,
#                  style={"width": "40%"}
#                  ),

#     html.Div(id="output_container", children=[]),
#     html.Br(),

#     dcc.Graph(id="my_bee_map", figure={})

# ])

# desafio B
app.layout = html.Div([
    html.H1("Web Application Dashboards with Dash",
            style={"text-align": "center"}),

    dcc.Dropdown(id="slct_cause",
                 options=[
                    {"label": "Disease", "value": "Disease"},
                    {"label": "Pesticides", "value": "Pesticides"},
                    {"label": "Pests_excl_Varroa", "value": "Pests_excl_Varroa"},
                    {"label": "Varroa_mites", "value": "Varroa_mites"},
                    {"label": "Unknown", "value": "Unknown"},
                    {"label": "Other", "value": "Other"}],
                 multi=False,
                 value="Disease",
                 style={"width": "40%"}
                 ),

    html.Div(id="output_container", children=[]),
    html.Br(),

    dcc.Graph(id="my_bee_map", figure={})

])

# conecta os graficos plotly com o app dash


@app.callback(
    [Output(component_id="output_container", component_property="children"),
     Output(component_id="my_bee_map", component_property="figure")],
    [Input(component_id="slct_cause", component_property="value")]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = f"The cause chosen by user was: {option_slctd}"

    state_list = ["Texas", "New Mexico", "New York"]
    dff = df.copy()
    dff = dff[dff["Affected by"] == option_slctd]
    dff_1 = dff[dff["State"].isin(state_list)]
    # dff_New_Mexico = dff[dff["State"] == ]
    # dff_New_York = dff[dff["State"] == ]

    # fig = px.choropleth(
    #     data_frame=dff,
    #     locationmode="USA-states",
    #     locations="state_code",
    #     scope="usa",
    #     color="Pct of Colonies Impacted",
    #     hover_data=["State", "Pct of Colonies Impacted"],
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={"Pct of Colonies Impacted": '% of Bee Colonies'},
    #     template="plotly_dark"
    # )

    # plotly graph obj
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )

    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope="usa"),
    # )

    # desafio A
    # fig = px.bar(
    #     dff, x='State', y='Pct of Colonies Impacted')

    # desafio B
    fig = px.line(dff_1, x="Year", y="Pct of Colonies Impacted", color='State')

    return container, fig


if __name__ == "__main__":
    app.run_server(debug=True)
