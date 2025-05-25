import pandas as pd
from bokeh.io import curdoc
from bokeh.models import Tabs
from hist import hist_tab

# Load dataset and clean NaNs
data = pd.read_csv('flights.csv').dropna(subset=['arr_delay', 'name'])

# Create histogram tab
tab_hist = hist_tab(data)

# Create tabs layout and add to Bokeh document
tabs = Tabs(tabs=[tab_hist])
curdoc().add_root(tabs)
curdoc().title = "Flight Delay Histogram"