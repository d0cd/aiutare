#!/usr/bin/env python3
import importlib
from subprocess import Popen
import mongoengine
import plotly
import plotly.graph_objs as go
from bin.config import config

Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
      " --replSet monitoring_replSet".split())

schemas = importlib.import_module(config["schemas"])
mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

names = ["syrup_stock", 'minisat_stock', 'minisat_clone', 'maple_stock']

sum_time_elapsed_sat = [0.0] * len(names)
sum_time_elapsed_unsat = [0.0] * len(names)

number_results_sat = [0] * len(names)
number_results_unsat = [0] * len(names)
number_results_timeout = [0] * len(names)

for result in schemas.Result.objects():
    index = names.index(result.nickname)
    if result.result == "sat":
        sum_time_elapsed_sat[index] += result.elapsed
        number_results_sat[index] += 1

    elif result.result == "unsat":
        sum_time_elapsed_unsat[index] += result.elapsed
        number_results_unsat[index] += 1

    elif result.elapsed == config["timeout"]:
        number_results_timeout[index] += 1

data = [None]*len(names)

for i in range(len(names)):
    data[i]= go.Bar(
        x=['sat', 'unsat', 'total'],
        y=[sum_time_elapsed_sat[i] / number_results_sat[i],
           sum_time_elapsed_unsat[i] / number_results_unsat[i],
           (sum_time_elapsed_sat[i]+sum_time_elapsed_unsat[i]+ config["timeout"]*number_results_timeout[i]
            )/(number_results_timeout[i]+number_results_sat[i]+number_results_unsat[i])],
        name=names[i]
    )

# Finish and create graph
layout = go.Layout(
    barmode='group'
)

plotly.offline.plot({
    "data": data,
    "layout": layout
}, auto_open=True, filename="plots/tester.html")

mongoengine.connection.disconnect()
