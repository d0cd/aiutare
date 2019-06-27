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

x_coords = []
y_coords = []
z_coords = []

for i in range(len(names)):
    x_coords.append([])
    y_coords.append([])
    z_coords.append([])


for result in schemas.Result.objects():
    index = names.index(result.nickname)
    if (result.result == "sat" and include_sat) or (result.result == "unsat" and include_unsat) or (result.elapsed ==
    config["timeout"] and include_timeout):
        y_coords[index].append(result.elapsed)
        x_coords[index].append(result.num_propagations)
        z_coords[index].append(result.num_conflicts)

data = []

for i in range(len(names)):
    if len(x_coords[i])>0:
        data.append(go.Scatter3d(
            x=x_coords[i],
            y=y_coords[i],
            z=z_coords[i],
            mode='markers',
            name=names[i]
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
