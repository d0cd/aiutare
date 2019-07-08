import mongoengine
from mongoengine import *
from bin.benching.config import config


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
    instance = ReferenceField(Instance, required=True)
    result = StringField(required=True)
    elapsed = FloatField(required=True)
    model = StringField()
    verified = StringField(choices=("YES", "NO", "N/A"))
    # YES means that the model is SAT according to all solvers
    # NO means that at least one solver returned UNSAT on the model
    # N/A means that the model has not been verified or disproved yet


# Formats and writes results to the database:
# ------------------------------------------------
def write_instances(instances):
    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not Instance.objects(filename=stripped_instance):

            Instance.objects(filename=stripped_instance). \
                update_one(upsert=True,
                           set__filename=stripped_instance)

    mongoengine.connection.disconnect()


# Formats and writes results to the database:
# ------------------------------------------------
def write_results(program, nickname, instance, result, elapsed, model):

    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

    split_filename = instance.split("/", 1)[1]
    this_instance = Instance.objects.get(filename=split_filename)

    this_result = Result(program=program)
    this_result.nickname = nickname
    this_result.instance = this_instance
    this_result.result = result
    this_result.elapsed = elapsed

    # For model verification
    if model:
        this_result.model = model
        this_result.verified = "N/A"

    this_result.save(force_insert=True)

    # Updates the current instance's counters with each result
    if result == 'sat':
        this_instance.modify(inc__num_sat=1)
    elif result == 'unsat':
        this_instance.modify(inc__num_unsat=1)
    else:
        this_instance.modify(inc__num_unknown=1)

    mongoengine.connection.disconnect()
