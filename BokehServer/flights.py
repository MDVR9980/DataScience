# flights.py
from bokeh.io import curdoc
from bokeh.models import Tabs
import pandas as pd
from hist import hist_tab

# Load dataset
data = pd.read_csv('flights.csv', index_col=0).dropna()

# Create histogram tab
tab_hist = hist_tab(data)

# Add to document
tabs = Tabs(tabs=[tab_hist])
curdoc().add_root(tabs)
