import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

output_file('thor_wwii.html')

data = pd.read_csv('thor_wwii.csv').sample(100)
dataSource = ColumnDataSource(data)

p = figure()
p.circle(source=dataSource, x='AC_ATTACKING', y='TOTAL_TONS', color='green', size='TONS_IC')

show(p)