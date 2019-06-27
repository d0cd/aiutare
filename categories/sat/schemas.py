import mongoengine
from mongoengine import *
import numpy as np
from bin.config import config


# MongoEngine schemas:
# ---------------------

class Instance(Document):
    filename = StringField(required=True)
    num_sat = IntField(default=0)
    num_unsat = IntField(default=0)
    num_unknown = IntField(default=0)

    # Information gathered from MiniSAT output
    num_variables = IntField(default=0)
    num_clauses = IntField(default=0)

    meta = {
        'indexes': [
            {'fields': ['filename'], 'unique': True}
        ]
    }


class Result(Document):
    program = StringField(required=True)
    nickname = StringField(required=True)
    # version = StringField()
    instance = ReferenceField(Instance, required=True)
    result = StringField(required=True)
    elapsed = FloatField(required=True)

    # Information gathered from MiniSAT output
    num_conflicts = FloatField()
    num_decisions = FloatField()
    num_propagations = FloatField()


# Formats and writes results to the database:
# ------------------------------------------------
def write_results(program, nickname, instance, result, elapsed, results_dict=None):

    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

    split_filename = instance.split("/", 1)[1]
    this_instance = Instance.objects.get(filename=split_filename)

    this_result = Result(program=program)
    this_result.nickname = nickname
    this_result.instance = this_instance
    this_result.result = result
    this_result.elapsed = elapsed

    if results_dict:
        this_result.num_conflicts = results_dict["num_conflicts"]
        this_result.num_decisions = results_dict["num_decisions"]
        this_result.num_propagations = results_dict["num_propagations"]

    this_result.save(force_insert=True)

    # Updates the current instance's counters with each result
    if result == 'sat':
        this_instance.modify(inc__num_sat=1)
    elif result == 'unsat':
        this_instance.modify(inc__num_unsat=1)
    else:
        this_instance.modify(inc__num_unknown=1)

    # Updates the current instance's variable and clause counts
    # TODO

    mongoengine.connection.disconnect()


# Function to parse data for analyze from the database:
# ------------------------------------------------------
def read_database():
    data = {}

    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")
    parsed_result = np.dtype([('Instance', '<U14'), ('Result', '<U7'), ('Time', '<f8')])
    for result in Result.objects():

        # Formats data for analyze
        new_data = np.array([(result.instance.filename, result.result, result.elapsed)], dtype=parsed_result)

        if result.nickname in data:
            data[result.nickname] = np.append(data[result.nickname], new_data)
        else:
            data[result.nickname] = new_data

    mongoengine.connection.disconnect()

    return data
