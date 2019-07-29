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


# Formats and writes results to the database:
# ------------------------------------------------
def write_instances(instances):
    reload(config_file)
    mongoengine.connect(config_file.config["database_name"], replicaset="monitoring_replSet")

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not Instance.objects(filename=stripped_instance):

            Instance.objects(filename=stripped_instance). \
                update_one(upsert=True,
                           set__filename=stripped_instance)

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

    # if results_dict:
    # TODO: if adding extra information to results_dict, add it to this_result here

    this_result.save(force_insert=True)

    # Updates the current instance's counters with each result
    if result == 'sat':
        this_instance.modify(inc__num_sat=1)
    elif result == 'unsat':
        this_instance.modify(inc__num_unsat=1)
    else:
        this_instance.modify(inc__num_unknown=1)

    mongoengine.connection.disconnect()
