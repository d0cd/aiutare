#!/usr/bin/env python3
import importlib
from subprocess import Popen, DEVNULL
import mongoengine
import plotly
import plotly.graph_objs as go
from operator import attrgetter
from bin.config import config


X_AXIS = "num_propagations"
Y_AXIS = "elapsed"
Z_AXIS = "memory_used_MB"


mongod = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
               " --replSet monitoring_replSet".split(), stdout=DEVNULL)

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

x_parser = attrgetter(X_AXIS)
y_parser = attrgetter(Y_AXIS)
z_parser = attrgetter(Z_AXIS)

for result in schemas.Result.objects():
    index = names.index(result.nickname)
    if (result.result == "sat" and include_sat) or \
            (result.result == "unsat" and include_unsat) or \
            (result.elapsed == config["timeout"] and include_timeout):
        x_coords[index].append(x_parser(result))
        y_coords[index].append(y_parser(result))
        z_coords[index].append(z_parser(result))

data = []

for i in range(len(names)):
    if len(x_coords[i]) > 0:
        data.append(go.Scatter3d(
            x=x_coords[i],
            y=y_coords[i],
            z=z_coords[i],
            mode='markers',
            name=names[i]
        ))

layout = go.Layout(
    scene=dict(
        xaxis=dict(
            title=X_AXIS),
        yaxis=dict(
            title=Y_AXIS),
        zaxis=dict(
            title=Z_AXIS), ),
)

plotly.offline.plot({
    "data": data,
    "layout": layout
}, auto_open=True, filename="plots/testerScatter3D.html")

mongoengine.connection.disconnect()

mongod.terminate()
