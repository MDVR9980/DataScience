import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10, Viridis256
from math import ceil

# Set the output HTML file
output_file('thor3.html')

# Load the entire dataset without sampling
data = pd.read_csv('thor_wwii.csv')
data = data[data['COUNTRY_FLYING_MISSION'].isin(('USA', 'GREAT BRITAIN'))]

# Group data by country and sum relevant columns
dataGrouped = data.groupby('COUNTRY_FLYING_MISSION')[['TOTAL_TONS', 'TONS_FRAG', 'TONS_IC', 'TONS_HE']].sum().reset_index()

# List of grouped countries
countries = dataGrouped['COUNTRY_FLYING_MISSION'].tolist()
num_countries = len(countries)

# Select color palette based on number of countries
if num_countries <= 10:
    palette = Category10[10]
else:
    palette = Viridis256

# If number of countries exceeds palette size, repeat or truncate colors
if num_countries > len(palette):
    multiplier = ceil(num_countries / len(palette))
    palette = (palette * multiplier)[:num_countries]

# Map each country to a specific color
color_map = dict(zip(countries, palette))
# Add a 'colors' column to the grouped data
dataGrouped['colors'] = [color_map[country] for country in countries]

# Create a data source for Bokeh plotting
dataSource = ColumnDataSource(dataGrouped)

# Create a figure with categorical x-axis
p = figure(
    x_range=countries,
    title="Total Tons by Country",
    height=600,
    width=1000
)

# Colors for the stack layers
stack_colors = palette[:3]  # First three colors for the three stacks

# Draw stacked bars with correct legend labels
renderers = p.vbar_stack(
    stackers=['TONS_FRAG', 'TONS_IC', 'TONS_HE'],
    x='COUNTRY_FLYING_MISSION',
    width=0.8 / num_countries,
    color=stack_colors,
    source=dataSource,
    legend_label=['قطعات', ' اشتعال زا', 'انفجار قوی']
)

# Uncomment to add hover tool if needed
# hover = HoverTool()
# hover.tooltips = [
#     ("Country", "@COUNTRY_FLYING_MISSION"),
#     ("Total Tons", "@TOTAL_TONS"),
#     ("Frag Tons", "@TONS_FRAG"),
#     ("IC Tons", "@TONS_IC"),
#     ("HE Tons", "@TONS_HE"),
# ]
# hover.mode = 'vline'
# p.add_tools(hover)

# Rotate x-axis labels for better readability
p.xaxis.major_label_orientation = 1  # 45 degrees in radians

# Show the plot
show(p)