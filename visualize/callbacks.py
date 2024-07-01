from dash import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import time

from data_loader import dates_ist, opens, highs, lows, closes, volumes, instrument


# Define callback function
def update_chart_callback(app):
    @app.callback(
        Output('candlestick-chart', 'figure'),
        [Input('date-slider', 'value'),
         Input('chart-type', 'value')]
    )
    def update_chart(slider_range, chart_type):
        start, end = slider_range
        
        # Add a delay to simulate debounce
        time.sleep(1)

        filtered_dates_ist = dates_ist[start:end]
        filtered_opens = opens[start:end]
        filtered_highs = highs[start:end]
        filtered_lows = lows[start:end]
        filtered_closes = closes[start:end]
        filtered_volumes = volumes[start:end]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.7, 0.3], vertical_spacing=0.05,
                            subplot_titles=(f"{instrument} {chart_type.capitalize()} Chart", "Volume"))

        if chart_type == 'candlestick':
            chart_trace = go.Candlestick(
                x=filtered_dates_ist,
                open=filtered_opens,
                high=filtered_highs,
                low=filtered_lows,
                close=filtered_closes,
                name="Candlestick",
                text=[
                    f"Timestamp: {t}<br>Open: {o}<br>High: {h}<br>Low: {l}<br>Close: {c}<br>Volume: {v}"
                    for t, o, h, l, c, v in zip(filtered_dates_ist, filtered_opens, filtered_highs, filtered_lows, filtered_closes, filtered_volumes)
                ],
                hoverinfo='text'
            )
        elif chart_type == 'line':
            chart_trace = go.Scatter(
                x=filtered_dates_ist,
                y=filtered_closes,
                mode='lines',
                name="Line",
                text=[
                    f"Timestamp: {t}<br>Close: {c}<br>Volume: {v}"
                    for t, c, v in zip(filtered_dates_ist, filtered_closes, filtered_volumes)
                ],
                hoverinfo='text'
            )

        fig.add_trace(chart_trace, row=1, col=1)

        # Add volume trace
        volume_trace = go.Bar(
            x=filtered_dates_ist,
            y=filtered_volumes,
            name="Volume",
            opacity=0.7,
            text=[f"Volume: {v}" for v in filtered_volumes],
            hoverinfo='text'
        )
        fig.add_trace(volume_trace, row=2, col=1)

        # Update layout
        fig.update_layout(
            title=f"{instrument} with Volume",
            xaxis=dict(title="Time (IST)", rangeslider=dict(visible=True), type="date"),
            yaxis=dict(title="Price"),
            yaxis2=dict(title="Volume"),
            hovermode='x unified',
            dragmode='zoom',
            margin=dict(l=0, r=0, t=50, b=0)
        )

        return fig
