from bokeh.palettes import Category20_16
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, Slider, RangeSlider, CheckboxGroup, TabPanel, Div, Paragraph
from bokeh.plotting import figure
from bokeh.layouts import column, row

def hist_tab(data):
    # Data preparation based on selections
    def make_data(selected_names, start_range, end_range, bin_size):
        df = pd.DataFrame(columns=['proportion', 'left', 'right', 'f_proportion', 'f_interval', 'name', 'color'])
        total_range = end_range - start_range

        for i, airline in enumerate(selected_names):
            subset = data[(data['name'] == airline) & 
                          (data['arr_delay'] >= start_range) & 
                          (data['arr_delay'] <= end_range)]
            if subset.empty:
                continue
            hist, edges = np.histogram(subset['arr_delay'], bins=int(total_range / bin_size), range=(start_range, end_range))
            if hist.sum() == 0:
                continue
            hist_df = pd.DataFrame({
                'proportion': hist / hist.sum(),
                'left': edges[:-1],
                'right': edges[1:]
            })
            hist_df['f_proportion'] = [f"{p:.5f}" for p in hist_df['proportion']]
            hist_df['f_interval'] = [f"{int(l)} to {int(r)} minutes" for l, r in zip(hist_df['left'], hist_df['right'])]
            hist_df['name'] = airline
            hist_df['color'] = Category20_16[i % len(Category20_16)]

            df = pd.concat([df, hist_df], ignore_index=True)

        return ColumnDataSource(df)

    # Build plot
    def make_plot(source):
        p = figure(title='تاخیر در پرواز', width=800, height=600, tools="pan,wheel_zoom,box_zoom,reset,save")
        p.quad(source=source, bottom=0, top='proportion', left='left', right='right',
               fill_color='color', line_color='white', fill_alpha=0.7, legend_field='name')
        p.legend.title = "Airline"
        p.legend.location = "top_right"
        p.xaxis.axis_label = "Delay (minutes)"
        p.yaxis.axis_label = "Proportion"
        p.y_range.start = 0
        return p

    # Calculate statistics summary
    def update_stats(selected_names, start_range, end_range):
        summary = []
        for airline in selected_names:
            subset = data[(data['name'] == airline) & 
                          (data['arr_delay'] >= start_range) & 
                          (data['arr_delay'] <= end_range)]
            count = len(subset)
            if count == 0:
                summary.append(f"{airline}: No data in range")
                continue
            mean_delay = subset['arr_delay'].mean()
            median_delay = subset['arr_delay'].median()
            summary.append(f"{airline}: Count={count}, Mean={mean_delay:.1f}, Median={median_delay:.1f}")
        return "<br>".join(summary)

    # Controls
    airline_names = sorted(data['name'].unique())
    checkbox = CheckboxGroup(labels=airline_names, active=list(range(min(5,len(airline_names)))))  # Select top 5 by default
    bin_slider = Slider(start=1, end=30, value=5, step=1, title="دانه‌بندی هیستوگرام (دقیقه)")
    range_slider = RangeSlider(start=-60, end=180, value=(-60, 120), step=5, title="بازه‌ی تاخیر (دقیقه)")

    # Initial data and plot
    selected_names = [checkbox.labels[i] for i in checkbox.active]
    source = make_data(selected_names, range_slider.value[0], range_slider.value[1], bin_slider.value)
    plot = make_plot(source)

    # Stats display using Paragraph, no 'style', use 'styles' or CSS in Div
    stats = Paragraph(text=update_stats(selected_names, range_slider.value[0], range_slider.value[1]), width=300)

    # Update function
    def update(attr, old, new):
        selected = [checkbox.labels[i] for i in checkbox.active]
        new_source = make_data(selected, range_slider.value[0], range_slider.value[1], bin_slider.value)
        source.data = new_source.data
        stats.text = update_stats(selected, range_slider.value[0], range_slider.value[1])

    # Link callbacks
    checkbox.on_change('active', update)
    bin_slider.on_change('value', update)
    range_slider.on_change('value', update)

    # Layout
    controls = column(
        Div(text="<b>فیلترها</b>", styles={'font-size': '16px', 'text-align': 'right'}),
        checkbox,
        bin_slider,
        range_slider,
        Div(text="<b>آمار تاخیر</b>", styles={'font-size': '16px', 'text-align': 'right', 'margin-top': '10px'}),
        stats,
        width=320
    )
    layout = row(controls, plot)

    return TabPanel(child=layout, title="پنل هیستوگرام")
