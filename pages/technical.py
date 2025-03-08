import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd

# Correctly register the page
dash.register_page(__name__, path="/technical")

# Load the CSV file
file_path = "data/stocks_price.csv"
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is in datetime format

dropdown_tickers = dcc.Dropdown(
    id='ticker-dropdown',
    options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
    multi=True,
    placeholder="Select Ticker(s)...",
    searchable=True
)

date_picker = dcc.DatePickerRange(
    id='date-picker',
    min_date_allowed=df['Date'].min(),
    max_date_allowed=df['Date'].max(),
    start_date=df['Date'].min(),
    end_date=df['Date'].max()
)

aggregation_radio = dcc.RadioItems(
    id='aggregation-radio',
    options=[
        {'label': 'Daily', 'value': 'day'},
        {'label': 'Monthly', 'value': 'month'}
    ],
    value='day',
    inline=True
)

layout = dbc.Container([
    html.H2("Business Analysis", className="text-center mt-4"),
    html.P("This page contains business analysis visualizations."),
    dbc.Row([
        dbc.Col([html.Label("Select Ticker(s):"), dropdown_tickers], width=4),
        dbc.Col([html.Label("Select Date Range:"), date_picker], width=4),
        dbc.Col([html.Label("Aggregate By:"), aggregation_radio], width=4)
    ], className="mb-4"),
    dcc.Graph(id='box-plot')
], fluid=True)


@callback(
    Output('box-plot', 'figure'),
    [
        Input('ticker-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('aggregation-radio', 'value')
    ]
)
def update_graph(selected_tickers, start_date, end_date, aggregation):
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if selected_tickers:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(selected_tickers)]

    if aggregation == 'month':
        filtered_df['Date'] = filtered_df['Date'].dt.to_period('M').astype(str)

    fig = px.box(
        filtered_df, x='Date', y='Value', color='Ticker',
        title="Stock Price Box Plot",
        labels={'Price': 'Stock Price', 'Date': 'Date'}
    )

    fig.update_layout(xaxis={'categoryorder': 'category ascending'})
    return fig
