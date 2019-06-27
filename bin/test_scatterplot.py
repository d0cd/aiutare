#!/usr/bin/env python3
import importlib
from subprocess import Popen
import mongoengine
import plotly
import plotly.graph_objs as go
from bin.config import config
import scipy
from scipy import stats
import numpy as np

Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
      " --replSet monitoring_replSet".split())

schemas = importlib.import_module(config["schemas"])
mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

include_sat = True
include_unsat = True
include_timeout = True

names = ["syrup_stock", 'minisat_stock', 'minisat_clone', 'maple_stock']

y_coords = []

x_coords = []

for i in range(4):
    x_coords.append([])
    y_coords.append([])


for result in schemas.Result.objects():
    index = names.index(result.nickname)
    if (result.result == "sat" and include_sat) or (result.result == "unsat" and include_unsat) or (result.elapsed ==
    config["timeout"] and include_timeout):
        y_coords[index].append(result.elapsed)
        x_coords[index].append(result.num_propagations)

data = [None]*(2*len(names))

for i in range(len(names)):
    data[i] = go.Scatter(
        x=x_coords[i],
        y=y_coords[i],
        mode='markers',
        name=names[i]
    )
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_coords[i],y_coords[i])
    if r_value^2>0.8:
        data[i+len(names)]= go.Scatter(
            x=[0.0,1.0],
            y=[intercept,slope+intercept],
            mode = 'line',
            name=(names[i]+"Regression Line")
        )



layout= go.Layout(
    hovermode= 'closest',
    xaxis= dict(
        title= 'num_propagations',
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title= 'time_elapsed',
        ticklen= 5,
        gridwidth= 2,
    )
)

plotly.offline.plot({
    "data": data,
    "layout": layout
}, auto_open=True, filename="images/testerScatter.html")

mongoengine.connection.disconnect()
