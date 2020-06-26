#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:15:32 2020

@author: carolina
"""
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.tools import HoverTool
from datetime import datetime
#from bokeh.charts import Bar

G=figure(title='Project Schedule',x_axis_type='datetime',width=8000,height=4000,y_range=timelines.bloque.tolist(),
        x_range=Range1d(timelines.fromDate.min(),timelines.toDate.max()), tools='save')

hover=HoverTool(tooltips="Task: @Item<br>\
Start: @Start<br>\
End: @End")
G.add_tools(hover)

timelines['ID']=timelines.index+0.8
timelines['ID1']=timelines.index+1.2
CDS=ColumnDataSource(timelines)
G.quad(left='fromDate', right='toDate', bottom='ID', top='ID1',source=CDS,color="red")
#G.rect(,"Item",source=CDS)
show(G)