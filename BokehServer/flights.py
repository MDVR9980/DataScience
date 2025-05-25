from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from os.path import dirname, join
import pandas as pd
from hist import hist_tab

data = pd.read_csv('flights.csv', index_col=0).dropna()

tab_hist = hist_tab(data)
tabs = Tabs(tabs=[tab_hist])
curdoc().add_root(tabs)