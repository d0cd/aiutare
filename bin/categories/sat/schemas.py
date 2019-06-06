import mongoengine
from mongoengine import *
import numpy as np


# MongoEngine schemas:
# ---------------------

class SATInstance(Document):
    filename = StringField(required=True)


class SATResult(Document):
    program = StringField(required=True)
    nickname = StringField()
    # command = StringField()
    # version = StringField()
    instance = ReferenceField(SATInstance, required=True)
    result = StringField(required=True)
    elapsed = FloatField(required=True)


# Function to parse data for analyze from the database
def read_database():
    data = {}

    mongoengine.connect('sat_database')
    parsed_result = np.dtype([('Instance', '<U14'), ('Result', '<U7'), ('Time', '<f8')])
    for result in SATResult.objects():

        new_data = np.array([(result.instance.filename, result.result, result.elapsed)], dtype=parsed_result)

        if result.nickname in data:
            data[result.nickname] = np.append(data[result.nickname], new_data)
        else:
            data[result.nickname] = new_data

    return data
