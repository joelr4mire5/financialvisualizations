import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from pages import home, technical, business, ml

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Financial Dashboard"

# Navigation Bar
navbar = dbc.NavbarSimple(
    brand="Finsights",
    brand_href="/",
    color="dark",
    dark=True,
)

# Page Router
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(
    dash.Output('page-content', 'children'),
    [dash.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == "/technical":
        return technical.layout
    elif pathname == "/business":
        return business.layout
    elif pathname == "/ml":
        return ml.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)
