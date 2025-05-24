import pandas as pd
from bokeh.io import curdoc
from bokeh.models import Tabs
from hist import hist_tab  # Import the histogram tab function from hist.py

# Read the flight delay data from CSV, dropping rows with missing values
data = pd.read_csv('flights.csv', index_col=0).dropna()

# Create the histogram tab using the provided data
tab_hist = hist_tab(data)

# Add the histogram tab to the Bokeh layout as a tab panel
tabs = Tabs(tabs=[tab_hist])

# Add the layout to the current Bokeh document to render it in the server
curdoc().add_root(tabs)
