from dash_html_components.Option import Option
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


df = pd.read_csv(
    "C:/Projetos_C/Dash/Tutorial/Dash-by-Plotly-master/Dash_Interactive_Graphs/Urban_Park_Ranger_Animal_Condition_Response.csv")

app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
        html.Label(["Region"]),
        dcc.Dropdown(
            id="my_dropdown",
            options=[
                {"label": "Manhattan", "value": "Manhattan"},
                {"label": "Brooklyn", "value": "Brooklyn"},
                {"label": "Queens", "value": "Queens"},
                {"label": "Staten Island", "value": "Staten Island"},
                {"label": "Bronx", "value": "Bronx"},
            ],
            value="Manhattan",
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),
    html.Div([
        html.Label(["NYC Calls for Animal Rescue"]),
        dcc.Dropdown(
            id="my_dropdown2",
            options=[
                {"label": "Action Taken by Ranger",
                    "value": "Final Ranger Action"},
                {"label": "Age", "value": "Age"},
                {"label": "Animal Health", "value": "Animal Condition"},
                {"label": "Borough", "value": "Borough"},
                {"label": "Species", "value": "Animal Class"},
                {"label": "Species Status", "value": "Species Status"},
            ],
            value="Animal Class",
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id="the_graph")
    ]),

])


@ app.callback(
    Output(component_id="the_graph", component_property="figure"),
    [Input(component_id="my_dropdown", component_property="value"),
     Input(component_id="my_dropdown2", component_property="value")]
)
def update_graph(my_dropdow, my_dropdow2):
    dff = df.copy()
    dff = dff[dff["Borough"] == my_dropdow]

    piechart = px.pie(
        data_frame=dff,
        names=my_dropdow2,
        hole=.3,
    )
    # piechart.update_traces(textinfo='percent+label')

    return (piechart)


if __name__ == "__main__":
    app.run_server(debug=True)
