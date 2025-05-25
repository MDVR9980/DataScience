from bokeh.palettes import Category20_20
import numpy as np
import pandas as pd
from bokeh.models import (
    ColumnDataSource, Slider, RangeSlider, CheckboxGroup, TabPanel, Div,
    HoverTool, DataTable, TableColumn, Button, Spacer
)
from bokeh.plotting import figure
from bokeh.layouts import column, row, layout
from bokeh.transform import dodge

# Create the histogram tab
def hist_tab(data):
    def make_data(selected_names, start_range, end_range, bin_size):
        df = pd.DataFrame(columns=['proportion', 'left', 'right', 'f_proportion', 'f_interval', 'name', 'color'])
        total_range = end_range - start_range
        for i, airline in enumerate(selected_names):
            subset = data[(data['name'] == airline) & 
                          (data['arr_delay'] >= start_range) & 
                          (data['arr_delay'] <= end_range)]
            if subset.empty:
                continue
            bins = max(1, int(total_range / bin_size))
            hist, edges = np.histogram(subset['arr_delay'], bins=bins, range=(start_range, end_range))
            if hist.sum() == 0:
                continue
            hist_df = pd.DataFrame({
                'proportion': hist / hist.sum(),
                'left': edges[:-1],
                'right': edges[1:]
            })
            hist_df['f_proportion'] = [f"{p*100:.2f}%" for p in hist_df['proportion']]
            hist_df['f_interval'] = [f"{int(l)} تا {int(r)} دقیقه" for l, r in zip(hist_df['left'], hist_df['right'])]
            hist_df['name'] = airline
            hist_df['color'] = Category20_20[i % len(Category20_20)]
            df = pd.concat([df, hist_df], ignore_index=True)
        return ColumnDataSource(df)

    def make_histogram(source):
        p = figure(title="تاخیر پرواز - هیستوگرام", width=800, height=450, tools="pan,wheel_zoom,box_zoom,reset,save")
        quad = p.quad(source=source, bottom=0, top='proportion', left='left', right='right',
                      fill_color='color', line_color='white', fill_alpha=0.8, legend_field='name')
        p.xaxis.axis_label = "تاخیر (دقیقه)"
        p.yaxis.axis_label = "درصد پروازها"
        p.y_range.start = 0
        p.legend.title = "شرکت‌های هواپیمایی"
        p.legend.location = "top_right"

        hover = HoverTool(renderers=[quad],
                          tooltips=[("شرکت", "@name"), ("بازه", "@f_interval"), ("درصد", "@f_proportion")])
        p.add_tools(hover)
        return p

    def make_stats_plot(selected_names, start_range, end_range):
        stats_rows = []
        for airline in selected_names:
            subset = data[(data['name'] == airline) & 
                          (data['arr_delay'] >= start_range) & 
                          (data['arr_delay'] <= end_range)]
            if len(subset) == 0:
                continue
            stats_rows.append({
                'name': airline,
                'mean_delay': subset['arr_delay'].mean(),
                'median_delay': subset['arr_delay'].median()
            })

        if not stats_rows:
            return figure(width=800, height=250, title="آمار تاخیر - داده‌ای موجود نیست")

        stats_df = pd.DataFrame(stats_rows)
        stats_df = stats_df.sort_values("mean_delay", ascending=False)
        source = ColumnDataSource(stats_df)

        p = figure(x_range=stats_df['name'], width=800, height=300,
                   title="مقایسه میانگین و میانه تاخیر پرواز (دقیقه)",
                   tools="pan,box_zoom,reset,save", toolbar_location="above")

        p.vbar(x=dodge('name', -0.15, range=p.x_range), top='mean_delay', width=0.25,
               source=source, color="#718dbf", legend_label="میانگین")

        p.vbar(x=dodge('name', 0.15, range=p.x_range), top='median_delay', width=0.25,
               source=source, color="#e84d60", legend_label="میانه")

        p.add_tools(HoverTool(
            tooltips=[
                ("شرکت", "@name"),
                ("میانگین تاخیر", "@mean_delay{0.0} دقیقه"),
                ("میانه تاخیر", "@median_delay{0.0} دقیقه"),
            ]
        ))

        p.yaxis.axis_label = "تاخیر (دقیقه)"
        p.xaxis.major_label_orientation = 1
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        p.legend.click_policy = "hide"

        return p

    def make_stats_table(selected_names, start_range, end_range):
        rows = []
        for airline in selected_names:
            subset = data[(data['name'] == airline) & 
                          (data['arr_delay'] >= start_range) & 
                          (data['arr_delay'] <= end_range)]
            count = len(subset)
            mean_delay = subset['arr_delay'].mean() if count > 0 else None
            median_delay = subset['arr_delay'].median() if count > 0 else None
            rows.append({
                "Airline": airline,
                "Count": count,
                "Mean Delay": f"{mean_delay:.2f}" if mean_delay is not None else "No Data",
                "Median Delay": f"{median_delay:.2f}" if median_delay is not None else "No Data"
            })
        df = pd.DataFrame(rows)
        source = ColumnDataSource(df)
        columns = [
            TableColumn(field="Airline", title="شرکت هواپیمایی"),
            TableColumn(field="Count", title="تعداد پروازها"),
            TableColumn(field="Mean Delay", title="میانگین تاخیر (دقیقه)"),
            TableColumn(field="Median Delay", title="میانه تاخیر (دقیقه)")
        ]
        return DataTable(source=source, columns=columns, width=700, height=200, index_position=None)

    def reset_filters():
        checkbox.active = list(range(min(5, len(airline_names))))
        bin_slider.value = 5
        range_slider.value = (-60, 120)

    def update(attr, old, new):
        selected = [checkbox.labels[i] for i in checkbox.active]
        new_source = make_data(selected, range_slider.value[0], range_slider.value[1], bin_slider.value)
        source.data = new_source.data

        # Replace the histogram plot
        new_hist_plot = make_histogram(source)
        main_layout.children[0].children[1] = new_hist_plot

        # Update the statistics text
        stats_paragraph.text = "<br>".join([
            f"{air}: تعداد={len(data[(data['name']==air) & (data['arr_delay'] >= range_slider.value[0]) & (data['arr_delay'] <= range_slider.value[1])])}" 
            for air in selected
        ])

        # Update the stats bar chart and table
        stats_layout.children[1] = make_stats_plot(selected, range_slider.value[0], range_slider.value[1])
        stats_layout.children[2] = make_stats_table(selected, range_slider.value[0], range_slider.value[1])

    # UI widgets
    airline_names = sorted(data['name'].unique())
    checkbox = CheckboxGroup(labels=airline_names, active=list(range(min(5, len(airline_names)))))
    bin_slider = Slider(start=1, end=30, value=5, step=1, title="Histogram Bin Size (Minutes)")
    range_slider = RangeSlider(start=-60, end=180, value=(-60, 120), step=5, title="Delay Range (Minutes)")
    reset_button = Button(label="Reset Filters", button_type="warning")
    reset_button.on_click(reset_filters)

    # Initial plots
    selected_names = [checkbox.labels[i] for i in checkbox.active]
    source = make_data(selected_names, range_slider.value[0], range_slider.value[1], bin_slider.value)
    hist_plot = make_histogram(source)
    stats_paragraph = Div(text="", width=700)

    stats_layout = column(
        Div(text="<b>Descriptive Statistics</b>", styles={'font-size': '16px', 'text-align': 'right'}),
        make_stats_plot(selected_names, range_slider.value[0], range_slider.value[1]),
        make_stats_table(selected_names, range_slider.value[0], range_slider.value[1])
    )

    # Set up widget interactions
    checkbox.on_change('active', update)
    bin_slider.on_change('value', update)
    range_slider.on_change('value', update)

    controls = column(
        Div(text="<b>Filters</b>", styles={'font-size': '18px', 'text-align': 'right', 'margin-bottom':'10px'}),
        checkbox,
        Spacer(height=10),
        bin_slider,
        range_slider,
        Spacer(height=10),
        reset_button,
        width=320,
        sizing_mode="fixed"
    )

    main_layout = layout([
        [controls, hist_plot],
        [Spacer(width=20), stats_layout]
    ], sizing_mode="stretch_width")

    return TabPanel(child=main_layout, title="Advanced Histogram Panel")