import mongoengine
from mongoengine import *
import numpy as np
import json


CONFIG = json.loads(open("bin/config.json", 'r').read())


# MongoEngine schemas:
# ---------------------

class Instance(Document):
    filename = StringField(required=True)
    num_sat = IntField(default=0)
    num_unsat = IntField(default=0)
    num_unknown = IntField(default=0)
    # TODO: add more fields here as needed

    meta = {
        'indexes': [
            {'fields': ['filename'], 'unique': True}
        ]
    }


class Result(Document):
    program = StringField(required=True)
    nickname = StringField()
    instance = ReferenceField(Instance, required=True)
    result = StringField(required=True)
    elapsed = FloatField(required=True)
    # TODO: add more fields here as needed
    output = StringField()
    model = StringField()


# Formats and writes information to the database:
# ------------------------------------------------
def write_results(program, nickname, instance, result, elapsed, output, model):

    mongoengine.connect(CONFIG["database_name"])

    split_filename = instance.split("/", 1)[1]
    this_instance = Instance.objects.get(filename=split_filename)

    this_result = Result(program=program)
    this_result.nickname = nickname
    this_result.instance = this_instance
    this_result.result = result
    this_result.elapsed = elapsed
    this_result.output = output
    this_result.model = model
    # TODO: write other data as specified by your schema here before saving
    this_result.save(force_insert=True)

    # Updates the current instance's counters with each result
    if result == 'sat':
        this_instance.modify(inc__num_sat=1)
    elif result == 'unsat':
        this_instance.modify(inc__num_unsat=1)
    else:
        this_instance.modify(inc__num_unknown=1)

    mongoengine.connection.disconnect()


# Function to parse data for analyze from the database:
# ------------------------------------------------------
def read_database():
    data = {}

    mongoengine.connect(CONFIG["database_name"])
    parsed_result = np.dtype([('Instance', '<U14'), ('Result', '<U7'), ('Time', '<f8')])  # TODO: update with schema
    for result in Result.objects():

        # TODO: this will need to be modified if passing additional info to analyze.py
        new_data = np.array([(result.instance.filename, result.result, result.elapsed)], dtype=parsed_result)

        if result.nickname in data:
            data[result.nickname] = np.append(data[result.nickname], new_data)
        else:
            data[result.nickname] = new_data

    mongoengine.connection.disconnect()

    return data
