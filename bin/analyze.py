#!/usr/bin/env python3
import importlib
from bin.benching.config import config


# AGGREGATION FUNCTIONS


def aggregate_times(data, average=True, include_overall=False):

    choices = ["sat", "unsat", "unknown", "error", "overall"]
    choices = choices if include_overall else choices[:-1]
    y_data_list = []
    solvers = []

    for solver, runs in data.items():
        solvers.append(solver)
        times = time_results(runs)

        if average:
            count = count_results(runs)
            count = [count[0], count[1], count[2], count[4]]  # remove timeouts
            count = count + [sum(count)] if include_overall else count

            for i in range(len(count)):
                times[i] = times[i] / count[i] if count[i] > 0 else 0

        y_data_list.append(times if include_overall else times[:-1])

    print_times(average, choices, solvers, y_data_list)


def aggregate_counts(data):

    choices = ["sat", "unsat", "unknown", "timeout", "error"]
    counts = []
    solvers = []

    for solver, runs in data.items():
        solvers.append(solver)
        counts.append(count_results(runs))

    print_counts(choices, solvers, counts)


# ANALYSIS AND AGGREGATION

def count_results(runs):
    choices = ["sat", "unsat", "unknown", "timeout", "error"]
    results = [0 for _ in choices]

    for r in runs["Result"]:
        if r == "sat":
            results[0] += 1
        if r == "unsat":
            results[1] += 1
        if r == "unknown":
            results[2] += 1
        if "timeout" in r:
            results[3] += 1
        if r == "error":
            results[4] += 1

    return results


def time_results(runs):
    choices = ["sat", "unsat", "unknown", "error", "overall"]
    results = [0 for _ in choices]

    for r in range(len(runs["Result"])):
        if runs["Result"][r] == "sat":
            results[0] += runs["Time"][r]
        if runs["Result"][r] == "unsat":
            results[1] += runs["Time"][r]
        if runs["Result"][r] == "unknown":
            results[2] += runs["Time"][r]
        if runs["Result"][r] == "error":
            results[3] += runs["Time"][r]
        results[4] += runs["Time"][r]

    return results


def check_consensus(data):
    # ASSUMING IN SAME ORDER!!!
    issues = []
    min_solved = min(len(runs) for solver, runs in data.items())

    for i in range(min_solved):
        votes = {}

        for solver, runs in data.items():
            votes[solver] = runs["Result"][i]
            problem = runs['Instance'][i]

        done = False
        for _, va in votes.items():
            if done:
                break
            for _, vb in votes.items():
                if done:
                    break
                if va != vb and va in ['sat', 'unsat'] and vb in ['sat', 'unsat']:
                    issues.append((problem, votes))
                    done = True
                    break

    print_consensus_issues(issues)


# PRINTING RESULTS

def print_consensus_issues(issues):
    if len(issues) == 0:
        return

    print("\nDisagreements (%d):" % len(issues))
    print("Instance,", ", ".join(solver for solver in issues[0][1].keys()))

    for i in issues:
        print("%s," % i[0], ", ".join(i[1][solver] for solver in i[1].keys()))


def print_counts(choices, solvers, counts):
    print("\nCounts:")
    print("solver,", ", ".join(c for c in choices))

    for i in range(len(counts)):
        print(", ".join(c for c in [solvers[i]] + list(map(str, counts[i]))))


def print_times(average, choices, solvers, times):
    print("\nAverage Times (s):") if average else print("\nTimes (s):")
    print("solver,", ", ".join(c for c in choices))

    for i in range(len(times)):
        print(", ".join(c for c in [solvers[i]] + list(map(repr, times[i]))))


def import_category():
    schemas = importlib.import_module(config["schemas"])
    return schemas.read_database()


# ENTRY POINT

def analyze():
    data = import_category()

    check_consensus(data)
    aggregate_counts(data)
    aggregate_times(data)
