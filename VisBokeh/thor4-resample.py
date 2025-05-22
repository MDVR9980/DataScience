import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10, Viridis256
from math import ceil

# Set the output HTML file
output_file('thor4-resample.html')

# Load the entire dataset without sampling
data = pd.read_csv('thor_wwii.csv')
data['MSNDATE'] = pd.to_datetime(data['MSNDATE'], format='%m/%d/%Y')

# Group data by MSNDATE and sum relevant columns
dataGrouped = data.groupby(pd.Grouper(key='MSNDATE', freq='M'))[['TOTAL_TONS', 'TONS_FRAG', 'TONS_IC', 'TONS_HE']].sum().reset_index()

# Create a data source for Bokeh plotting
dataSource = ColumnDataSource(dataGrouped)

# Create a figure with categorical x-axis
p = figure(
    x_axis_type='datetime',
)
p.line(x='MSNDATE', y='TOTAL_TONS', color='red', source=dataSource, legend_label='کل انفجار ها', line_width=2)

p.line(x='MSNDATE', y='TONS_IC', color='green', source=dataSource, legend_label='آتش زا', line_width=2)

p.line(x='MSNDATE', y='TONS_HE', color='blue', source=dataSource, legend_label='اشتعال قوی', line_width=2)

p.legend.click_policy = 'hide'

# Show the plot
show(p)