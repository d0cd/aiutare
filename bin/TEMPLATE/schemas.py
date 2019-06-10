import mongoengine
from mongoengine import *
import numpy as np


# MongoEngine schemas:
# ---------------------

class Instance(Document):
    filename = StringField(required=True)
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


# Parses all unique instances and writes them to the database
def write_instances(instances):
    mongoengine.connect('database_name')  # TODO: replace with name of your database here

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not Instance.objects(filename=stripped_instance):
            Instance.objects(filename=stripped_instance).update_one(upsert=True, set__filename=stripped_instance)

    mongoengine.connection.disconnect()


# Function to parse data for analyze from the database
def read_database():
    data = {}

    mongoengine.connect('database_name')  # TODO: replace with name of your database here
    parsed_result = np.dtype([('Instance', '<U14'), ('Result', '<U7'), ('Time', '<f8')])  # TODO: update with schema
    for result in Result.objects():

        # TODO: this will need to be modified if passing additional info to analyze.py
        new_data = np.array([(result.instance.filename, result.result, result.elapsed)], dtype=parsed_result)

        if result.nickname in data:
            data[result.nickname] = np.append(data[result.nickname], new_data)
        else:
            data[result.nickname] = new_data

    return data
