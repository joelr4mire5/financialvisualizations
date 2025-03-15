import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd

# Register Dash page
dash.register_page(__name__, path="/technical")

# Load and preprocess data
file_path = "data/stocks_price.csv"
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])

dropdown_tickers = dcc.Dropdown(
    id='ticker-dropdown',
    options=[{'label': ticker, 'value': ticker} for ticker in df['Ticker'].unique()],
    multi=True,
    placeholder="Select Ticker(s)...",
    searchable=True,
    className="custom-dropdown"
)

date_picker = dcc.DatePickerRange(
    id='date-picker',
    min_date_allowed=df['Date'].min(),
    max_date_allowed=df['Date'].max(),
    start_date=df['Date'].min(),
    end_date=df['Date'].max(),
    className="custom-datepicker"
)

aggregation_radio = dbc.RadioItems(
    id='aggregation-radio',
    options=[
        {'label': 'Daily', 'value': 'day'},
        {'label': 'Weekly', 'value': 'week'},
        {'label': 'Monthly', 'value': 'month'}
    ],
    value='day',
    inline=True,
    className="custom-radio"
)

indicator_dropdown = dcc.Dropdown(
    id='indicator-dropdown',
    options=[
        {'label': 'Average Price', 'value': 'avg'},
        {'label': '5-Day Moving Average', 'value': 'ma5'},
        {'label': 'Bollinger Bands', 'value': 'bollinger'}
    ],
    multi=True,
    placeholder="Select Indicators...",
    searchable=True,
    className="custom-dropdown"
)

layout = dbc.Container([
    html.H2("Business Analysis", className="text-center mt-4"),
    html.P("This page contains business analysis visualizations."),
    dbc.Row([
        dbc.Col([
            html.Label("Select Ticker(s):", className="custom-label"), dropdown_tickers,
            html.Label("Aggregate By:", className="custom-label mt-3"), aggregation_radio,
            html.Label("Indicators:", className="custom-label mt-3"), indicator_dropdown
        ], width=3, className="filter-column"),
        dbc.Col([
            html.Div([
                html.Div(date_picker, className="top-right-date-picker"),
                dcc.Graph(id='box-plot')
            ], style={"position": "relative"}),
            dcc.Graph(id='volume-plot')
        ], width=9)
    ], className="custom-filters"),
], fluid=True, className="custom-container")


@callback(
    [
        Output('box-plot', 'figure'),
        Output('volume-plot', 'figure')
    ],
    [
        Input('ticker-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('aggregation-radio', 'value'),
        Input('indicator-dropdown', 'value')
    ]
)
def update_graph(selected_tickers, start_date, end_date, aggregation, indicators):
    if not selected_tickers:
        return go.Figure(), go.Figure()

    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    filtered_df = filtered_df[filtered_df['Ticker'].isin(selected_tickers)]

    # Separate Close price and Volume data
    price_df = filtered_df[filtered_df['Metric'] == 'Close']
    volume_df = filtered_df[filtered_df['Metric'] == 'Volume']

    if aggregation == 'month':
        price_df['Date'] = price_df['Date'].dt.to_period('M').astype(str)
        volume_df = volume_df.groupby([volume_df['Date'].dt.to_period('M').astype(str), 'Ticker'])[
            'Price'].sum().reset_index()
    elif aggregation == 'week':
        price_df['Date'] = price_df['Date'].dt.strftime('%b-Week %U')
        volume_df = volume_df.groupby([volume_df['Date'].dt.strftime('%b-Week %U'), 'Ticker'])[
            'Price'].sum().reset_index()
    else:
        price_df['Date'] = price_df['Date'].dt.strftime('%Y-%m-%d')
        volume_df = volume_df.groupby([volume_df['Date'].dt.strftime('%Y-%m-%d'), 'Ticker'])[
            'Price'].sum().reset_index()

        # Box plot for prices
    price_fig = go.Figure()
    for ticker in selected_tickers:
        subset_price = price_df[price_df['Ticker'] == ticker]
        price_fig.add_trace(go.Box(y=subset_price['Price'], x=subset_price['Date'], name=ticker))

        if indicators:
            if 'avg' in indicators:
                avg_price = subset_price.groupby('Date')['Price'].mean()
                price_fig.add_trace(
                    go.Scatter(x=avg_price.index, y=avg_price, mode='lines', name=f'{ticker} Avg Price'))

            if 'ma5' in indicators:
                ma5 = subset_price['Price'].rolling(window=5, min_periods=1).mean()
                price_fig.add_trace(go.Scatter(x=subset_price['Date'], y=ma5, mode='lines', name=f'{ticker} MA5'))

            if 'bollinger' in indicators:
                rolling_mean = subset_price['Price'].rolling(window=20, min_periods=1).mean()
                rolling_std = subset_price['Price'].rolling(window=20, min_periods=1).std()
                upper_band = rolling_mean + (rolling_std * 2)
                lower_band = rolling_mean - (rolling_std * 2)
                price_fig.add_trace(
                    go.Scatter(x=subset_price['Date'], y=upper_band, mode='lines', name=f'{ticker} Upper BB',
                               line=dict(dash='dot')))
                price_fig.add_trace(
                    go.Scatter(x=subset_price['Date'], y=lower_band, mode='lines', name=f'{ticker} Lower BB',
                               line=dict(dash='dot')))

    price_fig.update_layout(
        title="Stock Price Analysis",
        xaxis={'categoryorder': 'category ascending', 'title': 'Date'},
        yaxis={'title': 'Stock Price'},
        template="plotly_dark",
        boxmode='group',
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(color='white')
    )


    # Solid Bar plot for aggregated volume
    volume_fig = go.Figure()
    for ticker in selected_tickers:
        subset_volume = volume_df[volume_df['Ticker'] == ticker]
        volume_fig.add_trace(go.Bar(
            x=subset_volume['Date'],
            y=subset_volume['Price'],
            name=f"{ticker} Volume",
            marker=dict(color='blue', opacity=0.8)
        ))

    volume_fig.update_layout(
        title="Stock Volume Analysis",
        xaxis={'categoryorder': 'category ascending', 'title': 'Date'},
        yaxis={'title': 'Volume'},
        template="plotly_dark",
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(color='white')
    )

    return price_fig, volume_fig
