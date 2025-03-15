import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, page_container

# Initialize Dash app with pages enabled
app = dash.Dash(
    __name__,
    use_pages=True,  # Enables automatic page detection
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY]
)
app.title = "Financial Dashboard"
server = app.server

# Navigation Bar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("Finsights", href="/", className="ms-2"),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Technical Analysis", href="/technical", active="exact")),
                dbc.NavItem(dbc.NavLink("Business Analysis", href="/business", active="exact")),
                dbc.NavItem(dbc.NavLink("ML Analysis", href="/ml", active="exact")),
            ],
            className="ms-auto", navbar=True
        ),
    ]),
    color="dark",
    dark=True,
    sticky="top"
)

# Page Router using Dash Pages
app.layout = html.Div([
    navbar,
    page_container  # Automatically loads the correct page
])

if __name__ == '__main__':
    app.run_server(debug=True)
