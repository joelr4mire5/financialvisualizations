import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import requests

dash.register_page(__name__, path="/")
# Sample Apple Press Release Image (Replace with a real image URL)
apple_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/1024px-Apple_logo_black.svg.png"

# Layout
layout = dbc.Container([
    html.H2("Latest Stock Market News", className="text-center mt-4 mb-4"),

    # Press Release Section
    dbc.Card([
        dbc.CardImg(src=apple_image_url, top=True, style={"width": "150px", "margin": "auto", "padding": "20px"}),
        dbc.CardBody([
            html.H5("PRESS RELEASE", className="text-muted text-center"),
            html.H4("Apple Reports First Quarter Results", className="text-center"),
            html.P("January 30, 2025", className="text-center text-muted"),

            html.P(
                "Apple today announced financial results for its fiscal 2025 first quarter ended December 28, 2024. "
                "The Company posted quarterly revenue of $124.3 billion, up 4% year over year, and quarterly diluted earnings per share of $2.40, up 10% year over year.",
                className="lead"
            ),

            html.Blockquote([
                html.P(
                    "“Today Apple is reporting our best quarter ever, with revenue of $124.3 billion, up 4 percent from a year ago,” "
                    "said Tim Cook, Apple’s CEO. “We were thrilled to bring customers our best-ever lineup of products and services during the holiday season.”"),
                html.Footer("— Tim Cook, CEO", className="blockquote-footer")
            ], className="blockquote"),

            html.P(
                "“Our record revenue and strong operating margins drove EPS to a new all-time record with double-digit growth and "
                "allowed us to return over $30 billion to shareholders,” said Kevan Parekh, Apple’s CFO."
            ),

            html.H5("Key Highlights", className="mt-4"),
            html.Ul([
                html.Li("All-time records for total company revenue and EPS."),
                html.Li("Services revenue reaches new all-time high."),
                html.Li("Installed base of active devices at an all-time high."),
                html.Li("Declared a cash dividend of $0.25 per share."),
                html.Li("Apple Intelligence expanding to more languages in April.")
            ], className="list-unstyled"),

            dbc.Button("Read Full Report", href="https://nr.apple.com/dB8y5Y7xG0",
                       color="primary", target="_blank", className="mt-3")
        ])
    ], className="shadow-lg p-3 mb-5 bg-white rounded"),

], fluid=True)