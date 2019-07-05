#!/usr/bin/env python3
import importlib
import mongoengine
from tabulate import tabulate
from bin.benching.config import config

COUNTS_INDEX = {
    "sat": 0,
    "unsat": 1,
    "unknown": 2,
    "timeout": 3,
    "error": 4,
}

TIME_INDEX = {
    "sat": 0,
    "unsat": 1,
    "unknown": 2,
    "error": 3,
    "overall": 4,  # This overall avg time INCLUDES timeouts
}


def update_consensus(result, consensus_dict, nickname_index):
    if result.instance not in consensus_dict:
        consensus_dict[result.instance] = [None] * len(NICKNAMES)

    consensus_dict[result.instance][nickname_index] = result.result


def update_counts(result, counts_dict):
    if "timeout" in result.result:
        counts_dict[result.nickname][COUNTS_INDEX["timeout"]] += 1
    else:
        counts_dict[result.nickname][COUNTS_INDEX[result.result]] += 1


def update_times(result, times_dict):
    if "timeout" not in result.result:
        times_dict[result.nickname][TIME_INDEX[result.result]] += result.elapsed

    times_dict[result.nickname][TIME_INDEX["overall"]] += result.elapsed


# Goes over all Results in the database, adding needed info to the 3 dicts
def iterate_results(schemas, consensus_dict, counts_dict, times_dict):
    nickname_index = {}
    for i in range(len(NICKNAMES)):
        nickname_index[NICKNAMES[i]] = i

    for result in schemas.Result.objects():
        update_consensus(result, consensus_dict, nickname_index[result.nickname])
        update_counts(result, counts_dict)
        update_times(result, times_dict)


def print_consensus(consensus_dict):
    rows = []

    # Only adds instances which have some disagreement
    # By default, ONLY prints conflicts between sat and unsat
    for instance, results in consensus_dict.items():
        stripped_results = [result for result in results if result == "sat" or result == "unsat"]
        if 0 < len(stripped_results) != stripped_results.count(stripped_results[0]):
            rows.append([instance.filename] + results)

    if len(rows) > 0:
        print("Disagreements (%d):" % len(rows))
        print('-' * (17 + len(str(len(rows)))))

        print(tabulate(rows, headers=["Instance"] + NICKNAMES))
        print("\n\n")


def print_counts(counts_dict):
    rows = []
    for nickname, results in counts_dict.items():
        rows.append([nickname] + results)

    print("Counts:")
    print('-' * 7)

    print(tabulate(rows, headers=["Solver"] + list(COUNTS_INDEX.keys())))
    print("\n\n")


def print_times(avg_times_dict):
    pass


def analyze():
    schemas = importlib.import_module(config["schemas"])

    global NICKNAMES
    NICKNAMES = []
    for program in list(config["commands"].values()):
        NICKNAMES += list(program.keys())

    consensus_dict = {}
    counts_dict = dict.fromkeys(NICKNAMES, ([0] * 5))
    times_dict = dict.fromkeys(NICKNAMES, ([0.0] * 5))

    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

    iterate_results(schemas, consensus_dict, counts_dict, times_dict)

    mongoengine.connection.disconnect()

    print_consensus(consensus_dict)
    print_counts(counts_dict)
    print_times(times_dict)
