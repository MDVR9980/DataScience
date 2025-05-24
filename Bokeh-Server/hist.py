from bokeh.palettes import Category20_16
from bokeh.models.layouts import CheckboxGroup, CheckboxButtonGroup
import pandas as pd 
import numpy as np
from bokeh.models import ColumndataSource
from bokeh.plotting import figure
def hist_tab(data):
    
    def md(s_data, rs=-60, re=120, bin=10):
        d = pd.DataFrame(column=['proportion', 'left', 'right', 'f_proportion', 'f_interval', 'name', 'color'])
        r = re - rs
        for i, r_data in enumerate(s_data): 
            subset = data[data['name'] == r_data]
            arr_hist, edge = np.histogram(subset['arr_delay'], bins=int(r / bin), range=(rs, re))
            arr_df = pd.DataFrame({
                'proportion': arr_hist / np.sum(arr_hist), 
                'left': edge[:-1],
                'right': edge[1:]
            })  
            arr_df['f_proportion'] = ['%0.5f' % p for p in arr_df['proportion']]
            arr_df['f_interval'] = ['%d to %d minutes'(left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
            arr_df['name'] = r_data
            arr_df['color'] = Category20_16[i]    
            d = d.append(arr_df)
            
        d = d.sort_values(['name', 'left']) 
        d = ColumndataSource(d) 
        return d  
    
    def mp(s_data):
        p = figure(plot_width=700, plot_height=700, title='تاخیر در پرواز')
        p.quad(source=s_data, botton=0, top='proportion', left='left', right='right', color='color', fill_alpha=0.7, legend_label='name')
        return p
        
        
    def chbox_update(attr, old, new):
        air_lines_checked = [chbox.labels[i] for i in chbox.active]
        ds = md(air_lines_checked)
        
        
        
    air_lines = list(set(data['name']))
    air_lines.sort()
    colors = Category20_16
    colors.sort()
    
    chbox = CheckboxGroup(labels=air_lines), active=[0, 1] 
    chbox.on_change('active', chbox_update)
    
    ###
    init_data = [chbox.labels[i] for i in chbox.active]
    src = md(init_data)
    p = mp(src)
    