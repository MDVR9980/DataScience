from bokeh.palettes import Category20_16
from bokeh.models import CheckboxGroup
import pandas as pd 
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import Slider, RangeSlider
from bokeh.layouts import column, row
from bokeh.models.ui import Panel

def hist_tab(data):
    def md(s_data, rs=-60, re=120, bin=10):
        d = pd.DataFrame(columns=[
            'proportion', 'left', 'right', 'f_proportion', 'f_interval', 'name', 'color'
        ])

        r = re - rs
        for i, r_data in enumerate(s_data): 
            subset = data[data['name'] == r_data]
            # Avoid division by zero
            arr_hist, edge = np.histogram(subset['arr_delay'], bins=int(r / bin), range=(rs, re))
            arr_df = pd.DataFrame({
                'proportion': arr_hist / np.sum(arr_hist) if np.sum(arr_hist) != 0 else np.zeros_like(arr_hist),
                'left': edge[:-1],
                'right': edge[1:]
            })
            arr_df['f_proportion'] = ['%0.5f' % p for p in arr_df['proportion']]
            arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
            arr_df['name'] = r_data
            arr_df['color'] = Category20_16[i % len(Category20_16)]
            d = pd.concat([d, arr_df], ignore_index=True)

        d = d.sort_values(['name', 'left'])
        return ColumnDataSource(d)

    def mp(s_data):
        p = figure(width=700, height=700, title='تاخیر در پرواز')
        p.quad(source=s_data, bottom=0, top='proportion', left='left', right='right', color='color', fill_alpha=0.7, legend_field='name')
        p.legend.click_policy = "hide"
        return p

    def update(attr, old, new):
        # Get checked airlines
        air_lines_checked = [chbox.labels[i] for i in chbox.active]
        # Generate new data source
        new_source = md(air_lines_checked,
                        rs=range_slider.value[0],
                        re=range_slider.value[1],
                        bin=slider.value)
        # Update plot data
        p.renderers[0].data_source.data = new_source.data

    # List of airline names
    air_lines = sorted(set(data['name']))
    # Checkbox group for airline selection
    chbox = CheckboxGroup(labels=air_lines, active=list(range(min(2, len(air_lines)))))
    chbox.on_change('active', update)

    # Histogram bin size slider
    slider = Slider(start=1, end=30, step=1, value=5, title='دانه بندی هیستوگرام')
    slider.on_change('value', update)

    # Delay range slider
    range_slider = RangeSlider(start=-60, end=180, value=(-60, 120), step=5, title='بازه تاخیرها')
    range_slider.on_change('value', update)

    # Initialize data for plot
    init_data = [chbox.labels[i] for i in chbox.active]
    src = md(init_data, rs=range_slider.value[0], re=range_slider.value[1], bin=slider.value)

    # Create the plot
    p = mp(src)

    # Layouts
    controls = column(chbox, slider, range_slider)
    layout = row(controls, p)


    tab = Panel(child=layout)

    return tab