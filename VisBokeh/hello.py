from bokeh.plotting import figure, output_file, show

# Specify the output HTML file
output_file('hello.html')

# Define data points
x1 = [5, 6, 9, 10, 100, 130, 141]
x2 = [8, 10, 18, 20, 30, 100, 101]

# Create a new figure with title and axes labels
p = figure(title='Sample Line Plot', x_axis_label='X Axis', y_axis_label='Y Axis')

# Plot a blue line
p.line(x1, x2, color='blue', legend_label='دمای هوا')

# Plot green circles with size and transparency for better visibility
p.circle(x1, x2, color='green', size=5, alpha=0.7, legend_label='دمای هوای دایره ای')

# Enable legend click to hide/show glyphs
p.legend.click_policy = 'hide'

# Show the plot
show(p)