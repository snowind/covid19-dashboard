import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from function import *

app = dash.Dash(__name__)
server = app.server

app.layout =