import dash
import dash_bootstrap_components as dbc
from dash import html

# Correctly register the page
dash.register_page(__name__, path="/business")

layout = dbc.Container([
    html.H2("Business Analysis", className="text-center mt-4"),
    html.P("This page contains business analysis visualizations."),
], fluid=True)