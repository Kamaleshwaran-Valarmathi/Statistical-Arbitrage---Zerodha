from dash import dcc, html

from data_loader import dates_ist


layout = html.Div([
    html.Div(
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Candlestick', 'value': 'candlestick'},
                {'label': 'Line', 'value': 'line'}
            ],
            value='candlestick',
            style={'width': '200px'}
        ),
        style={'display': 'inline-block', 'padding': '10px'}
    ),
    html.Div(
        dcc.Graph(id='candlestick-chart', style={'flex': '1 1 auto'}),
        style={'display': 'flex', 'flexDirection': 'column', 'height': '80vh'}
    ),
    html.Div(
        dcc.RangeSlider(
            id='date-slider',
            min=0,
            max=len(dates_ist) - 1,
            value=[0, 1000],
            marks={i: {'label': str(dates_ist[i].strftime('%Y-%m-%d')), 'style': {'transform': 'rotate(90deg)'}}
                   for i in range(0, len(dates_ist), int(len(dates_ist) / 10))},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        style={'padding': '10px'}
    )
])
