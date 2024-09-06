from dash import Dash
from layout import layout
from callbacks import register_callbacks

# Initialize the Dash app
app = Dash(__name__)

# Set the layout from the separate layout file
app.layout = layout

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)