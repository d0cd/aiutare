#!/usr/bin/env python3
import importlib
import mongoengine
import plotly
import plotly.graph_objs as go
from bin.benching.config import config
from scipy import stats
from operator import attrgetter
import numpy as np

INCLUDE_SAT = True
INCLUDE_UNSAT = False
INCLUDE_TIMEOUT = False
INCLUDE_ERROR = False
INCLUDE_UNKNOWN = False

AXIS_OPTIONS = ["elapsed", "nickname"]

X_AXIS = "nickname"
Y_AXIS = "elapsed"

NICKNAME_VALS = {
    "z3_master": 1,
    "z3_federico": 2,
    "z3_seq": 3,
    "cvc4_models": 4,
    "cvc4_no_models": 5,
}

X_COORDS = []
Y_COORDS = []

DATA = []


def initialize_coords(names, schemas):
    for i in range(len(names)):
        X_COORDS.append([])
        Y_COORDS.append([])

    x_parser = attrgetter(X_AXIS)
    y_parser = attrgetter(Y_AXIS)

    for result in schemas.Result.objects():
        index = names.index(result.nickname)
        if (result.result == "sat" and INCLUDE_SAT) or \
                (result.result == "unsat" and INCLUDE_UNSAT) or \
                (result.elapsed == config["timeout"] and INCLUDE_TIMEOUT) or \
                (result.result == "error" and INCLUDE_ERROR) or\
                (result.result == "unknown" and INCLUDE_UNKNOWN):
            # X_COORDS[index].append(x_parser(result))
            X_COORDS[index].append(NICKNAME_VALS[x_parser(result)])
            Y_COORDS[index].append(y_parser(result))

    for i in range(len(names)):
        counter = 0
        while counter < len(X_COORDS[i]):
            if X_COORDS[i][counter] is None or Y_COORDS[i][counter] is None:
                X_COORDS[i].pop(counter)
                Y_COORDS[i].pop(counter)
            else:
                counter += 1


def quadratic_r_squared(i):
    z = np.polyfit(X_COORDS[i], Y_COORDS[i], 2)
    f = np.poly1d(z)

    yhat = f(X_COORDS[i])
    ybar = np.sum(Y_COORDS[i]) / len(Y_COORDS[i])
    ssreg = np.sum((yhat - ybar) ** 2)
    sstot = sum([(yi - ybar) ** 2 for yi in Y_COORDS[i]])
    r_squared = ssreg / sstot
    return r_squared


def linear_regress(i, names):
    slope, intercept, r_value, p_value, std_err = stats.linregress(X_COORDS[i], Y_COORDS[i])
    DATA.append(go.Scatter(
        x=[0.0, max(X_COORDS[i])],
        y=[intercept, slope * max(X_COORDS[i]) + intercept],
        mode='lines',
        name=(names[i] + " Regression Line Linear")
    ))


def exp_regress(i, names):
    slope, intercept, r_value, p_value, std_err = stats.linregress(X_COORDS[i], np.log(Y_COORDS[i]))
    x_coords_tmp = np.linspace(0, max(X_COORDS[i]), 200)
    y_coords_tmp = np.exp(slope * x_coords_tmp + intercept)
    DATA.append(go.Scatter(
        x=x_coords_tmp,
        y=y_coords_tmp,
        mode='lines',
        name=(names[i] + " Regression Line Exponential")
    ))


def quadratic_regress(i, names):
    z = np.polyfit(X_COORDS[i], Y_COORDS[i], 2)
    f = np.poly1d(z)
    x_coords_tmp = np.linspace(0, max(X_COORDS[i]), 200)
    y_coords_tmp = f(x_coords_tmp)

    DATA.append(go.Scatter(
        x=x_coords_tmp,
        y=y_coords_tmp,
        mode='lines',
        name=(names[i] + " Regression Line Quadratic")
    ))


def graph_lines():
    layout = go.Layout(
        hovermode='closest',
        xaxis=dict(
            title=X_AXIS,
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title=Y_AXIS,
            ticklen=5,
            gridwidth=2,
        )
    )

    plotly.offline.plot({
        "data": DATA,
        "layout": layout
    }, auto_open=True, filename="plots/testerScatter.html")


def scatterplot():

    schemas = importlib.import_module(config["schemas"])
    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

    nicknames = [nickname for programs, specifications in config["commands"].items() for
                 nickname, command in specifications.items()]

    initialize_coords(nicknames, schemas)

    for i in range(len(nicknames)):
        if not (len(X_COORDS[i]) == 0 or not len(X_COORDS[i]) == len(Y_COORDS[i])):
            DATA.append(go.Scatter(
                x=X_COORDS[i],
                y=Y_COORDS[i],
                mode='markers',
                name=nicknames[i]
            ))

            arr_r_squared = [0.0, 0.0, 0.0]

            arr_r_squared[0] = stats.linregress(X_COORDS[i], Y_COORDS[i])[2]
            arr_r_squared[1] = quadratic_r_squared(i)
            arr_r_squared[2] = stats.linregress(X_COORDS[i], np.log(Y_COORDS[i]))[2]

            optimal_fit = arr_r_squared.index(max(arr_r_squared))

            if optimal_fit == 0:
                linear_regress(i, nicknames)
            elif optimal_fit == 1:
                quadratic_regress(i, nicknames)
            else:
                exp_regress(i, nicknames)

    graph_lines()

    mongoengine.connection.disconnect()
