from dash import Dash

from callbacks import update_chart_callback
from layout import layout


# Initialize the Dash app
app = Dash(__name__)

# Set the layout for the app
app.layout = layout

# Register callbacks
update_chart_callback(app)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
