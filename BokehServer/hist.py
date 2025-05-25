# hist.py
from bokeh.palettes import Category20_16
from bokeh.models import CheckboxGroup, Slider, RangeSlider, ColumnDataSource, TabPanel
from bokeh.plotting import figure
from bokeh.layouts import column, row
import numpy as np
import pandas as pd

def hist_tab(data):

    def md(s_data, rs=-60, re=120, bin=10):
        hist_dfs = []
        r = re - rs
        for i, r_data in enumerate(s_data):
            subset = data[data['name'] == r_data]
            arr_hist, edge = np.histogram(subset['arr_delay'], bins=int(r / bin), range=(rs, re))
            arr_df = pd.DataFrame({
                'proportion': arr_hist / np.sum(arr_hist),
                'left': edge[:-1],
                'right': edge[1:]
            })
            arr_df['f_proportoin'] = ['%0.5f' % p for p in arr_df['proportion']]
            arr_df['f_interval'] = [f'{left} to {right} minutes' for left, right in zip(arr_df['left'], arr_df['right'])]
            arr_df['name'] = r_data
            arr_df['color'] = Category20_16[i % len(Category20_16)]
            hist_dfs.append(arr_df)
        d = pd.concat(hist_dfs).sort_values(['name', 'left'])
        return ColumnDataSource(d)

    def mp(s_data):
        p = figure(width=700, height=700, title='تاخیر در پرواز')
        p.quad(source=s_data, bottom=0, top='proportion', left='left', right='right',
               color='color', fill_alpha=0.7, legend_field='name')
        p.legend.click_policy = 'hide'
        return p

    def update(attr, old, new):
        air_lines_checked = [chbox.labels[i] for i in chbox.active]
        new_src = md(air_lines_checked, range_slider.value[0], range_slider.value[1], slider.value)
        src.data.update(new_src.data)

    air_lines = sorted(data['name'].unique())
    chbox = CheckboxGroup(labels=air_lines, active=[0, 1])
    chbox.on_change('active', update)

    slider = Slider(start=1, end=30, step=1, value=5, title='دانه‌بندی هیستوگرام')
    slider.on_change('value', update)

    range_slider = RangeSlider(start=-60, end=180, value=(-60, 120), step=5, title='بازه‌ی تاخیرها')
    range_slider.on_change('value', update)

    init_data = [chbox.labels[i] for i in chbox.active]
    src = md(init_data)
    p = mp(src)

    w = column(chbox, slider, range_slider)
    l = row(w, p)
    return TabPanel(child=l, title='پنل هیستوگرام')