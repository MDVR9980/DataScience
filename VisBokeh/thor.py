import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

output_file('thor_wwii.html')

data = pd.read_csv('thor_wwii.csv').sample(100)
dataSource = ColumnDataSource(data)

p = figure()
p.circle(source=dataSource, x='AC_ATTACKING', y='TOTAL_TONS', color='green', size='TONS_IC')

p.title = 'عملیات هوایی جنگ ‌های جهانی دوم'
p.xaxis.axis_label = 'تعداد نیروهای هوایی'
p.yaxis.axis_label = 'حجم انفجار'

h = HoverTool()
h.tooltips = [
    ('تاریخ حمله', '@MSNDATE'),
    ('نیروی هوایی', '@AIRCRAFT_NAME'),
    ('کشور اعزام کننده', '@COUNTRY_FLYING_MISSION')
]
p.add_tools(h)

show(p)