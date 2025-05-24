from bokeh.palettes import Category20_16
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, Slider, RangeSlider, CheckboxGroup, TabPanel, Div
from bokeh.plotting import figure
from bokeh.layouts import column, row

def hist_tab(data):

    def make_data(selected_names, start_range, end_range, bin_size):
        df = pd.DataFrame(columns=['proportion', 'left', 'right', 'f_proportion', 'f_interval', 'name', 'color'])
        total_range = end_range - start_range

        for i, airline in enumerate(selected_names):
            subset = data[data['name'] == airline]
            hist, edges = np.histogram(subset['arr_delay'], bins=int(total_range / bin_size), range=(start_range, end_range))
            hist_df = pd.DataFrame({
                'proportion': hist / np.sum(hist),
                'left': edges[:-1],
                'right': edges[1:]
            })
            hist_df['f_proportion'] = [f"{p:.5f}" for p in hist_df['proportion']]
            hist_df['f_interval'] = [f"{int(l)} to {int(r)} minutes" for l, r in zip(hist_df['left'], hist_df['right'])]
            hist_df['name'] = airline
            hist_df['color'] = Category20_16[i % len(Category20_16)]

            df = pd.concat([df, hist_df], ignore_index=True)

        return ColumnDataSource(df)

    def make_plot(source):
        p = figure(title='تاخیر در پرواز', width=800, height=600, tools="pan,wheel_zoom,box_zoom,reset,save")
        p.quad(source=source, bottom=0, top='proportion', left='left', right='right',
               fill_color='color', line_color='white', fill_alpha=0.7, legend_field='name')
        p.legend.title = "Airline"
        p.legend.location = "top_right"
        p.xaxis.axis_label = "Delay (minutes)"
        p.yaxis.axis_label = "Proportion"
        return p

    # کنترل‌ها
    airline_names = sorted(data['name'].unique().tolist())
    checkbox = CheckboxGroup(labels=airline_names, active=[0, 1])
    bin_slider = Slider(start=1, end=30, value=5, step=1, title="دانه‌بندی هیستوگرام (minutes)")
    range_slider = RangeSlider(start=-60, end=180, value=(-60, 120), step=5, title="بازه‌ی تاخیر")

    # منبع داده اولیه
    initial_names = [checkbox.labels[i] for i in checkbox.active]
    source = make_data(initial_names, range_slider.value[0], range_slider.value[1], bin_slider.value)
    plot = make_plot(source)

    # تابع بروزرسانی
    def update(attr, old, new):
        selected = [checkbox.labels[i] for i in checkbox.active]
        src_new = make_data(selected, range_slider.value[0], range_slider.value[1], bin_slider.value)
        source.data = src_new.data

    # اتصال کنترل‌ها به تابع بروزرسانی
    checkbox.on_change('active', update)
    bin_slider.on_change('value', update)
    range_slider.on_change('value', update)

    controls = column(Div(text="<b>فیلترها</b>", styles={'font-size': '16px'}), checkbox, bin_slider, range_slider, width=300)
    layout = row(controls, plot)
    return TabPanel(child=layout, title="پنل هیستوگرام")