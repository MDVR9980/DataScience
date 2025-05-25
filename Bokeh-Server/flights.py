import pandas as pd
from bokeh.io import curdoc
from bokeh.models import Tabs
from hist import hist_tab

data = pd.read_csv('flights.csv').dropna(subset=['arr_delay', 'name'])

tab_hist = hist_tab(data)

tabs = Tabs(tabs=[tab_hist])

curdoc().add_root(tabs)
