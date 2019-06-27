#!/usr/bin/env python3
import importlib
from subprocess import Popen
import mongoengine
import plotly
import plotly.graph_objs as go
from bin.config import config
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

for i in range(len(names)):
    x_coords.append([])
    y_coords.append([])


for result in schemas.Result.objects():
    index = names.index(result.nickname)
    if (result.result == "sat" and include_sat) or (result.result == "unsat" and include_unsat) or (result.elapsed ==
    config["timeout"] and include_timeout):
        y_coords[index].append(result.elapsed)
        x_coords[index].append(result.num_propagations)

data = []

for i in range(len(names)):
    if len(x_coords)>0:
        data.append(go.Scatter(
            x=x_coords[i],
            y=y_coords[i],
            mode='markers',
            name=names[i]
        ))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_coords[i],y_coords[i])
        if r_value**2>0.8:
            data.append(go.Scatter(
                x=[0.0,max(x_coords[i])],
                y=[intercept,slope * max(x_coords[i])+intercept],
                mode = 'lines',
                name=(names[i]+" Regression Line")
            ))
        else:
            z = np.polyfit(x_coords[i], y_coords[i], 2)
            f = np.poly1d(z)
            x_coords_tmp = np.linspace(0,max(x_coords[i]),200)
            y_coords_tmp = f(x_coords_tmp)
            data.append(go.Scatter(
                x=x_coords_tmp,
                y=y_coords_tmp,
                mode = 'lines',
                name = (names[i]+" Regression Line")
            ))


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
