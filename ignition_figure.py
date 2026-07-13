from dash import Dash, html, dcc
from figures.ignition import make_ignition_figure

app = Dash(__name__)
server = app.server

fig = make_ignition_figure()

app.layout = html.Div([
    html.H1("Phoenix Ignition", style={"textAlign": "center"}),
    dcc.Graph(figure=fig, id="ignition-geometry"),
])
