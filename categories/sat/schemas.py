import mongoengine
from mongoengine import *
from importlib import reload
import bin.benching.config as config_file


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

    # Information extracted from program output
    num_conflicts = FloatField()
    num_decisions = FloatField()
    num_propagations = FloatField()
    memory_used_MB = FloatField()


# Parses out num_variables and num_clauses from a CNF file header
# -----------------------------------------------------------------
def parse_cnf(instance):
    with open(instance, "r") as f:
        arr_lines = f.readlines()

        for line in arr_lines:
            if line[0] == 'p':
                line_arr = line.split()
                num_variables = line_arr[2]
                num_clauses = line_arr[3]

    return num_variables, num_clauses


# Formats and writes results to the database:
# ------------------------------------------------
def write_instances(instances):
    reload(config_file)
    mongoengine.connect(config_file.config["database_name"], replicaset="monitoring_replSet")

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not Instance.objects(filename=stripped_instance):
            num_variables, num_clauses = parse_cnf(instance)

            Instance.objects(filename=stripped_instance). \
                update_one(upsert=True,
                           set__filename=stripped_instance,
                           set__num_variables=num_variables,
                           set__num_clauses=num_clauses)

    mongoengine.connection.disconnect()


# Formats and writes results to the database:
# ------------------------------------------------
def write_results(program, nickname, instance, result, elapsed, results_dict=None):
    reload(config_file)
    mongoengine.connect(config_file.config["database_name"], replicaset="monitoring_replSet")

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
        this_result.memory_used_MB = results_dict["memory_used_MB"]

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
