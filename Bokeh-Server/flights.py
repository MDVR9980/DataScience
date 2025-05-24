import pandas as pd
from bokeh.io import curdoc
from bokeh.models import Tabs
from hist import hist_tab

# خواندن داده‌ها
data = pd.read_csv('flights.csv', index_col=0).dropna()

# ساختن تب هیستوگرام
tab_hist = hist_tab(data)

# قرار دادن تب در صفحه
tabs = Tabs(tabs=[tab_hist])
curdoc().add_root(tabs)
