import mongoengine
from mongoengine import *
import numpy as np
import json


CONFIG = json.loads(open("bin/config.json", 'r').read())


# MongoEngine schemas:
# ---------------------

class Instance(Document):
    filename = StringField(required=True)
    num_sat = IntField()
    num_unsat = IntField()
    num_unknown = IntField()

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


# Function to parse data for analyze from the database:
# ------------------------------------------------------
def read_database():
    data = {}

    mongoengine.connect(CONFIG["database_name"])
    parsed_result = np.dtype([('Instance', '<U14'), ('Result', '<U7'), ('Time', '<f8')])
    for result in Result.objects():

        # Formats data for analyze
        new_data = np.array([(result.instance.filename, result.result, result.elapsed)], dtype=parsed_result)

        if result.nickname in data:
            data[result.nickname] = np.append(data[result.nickname], new_data)
        else:
            data[result.nickname] = new_data

        # Updates the current instance's counters with each result
        cur_instance = Instance.objects.get(filename=result.instance.filename)
        if result.result == 'sat':
            Instance.objects(filename=result.instance.filename).\
                update_one(set__num_sat=cur_instance.num_sat + 1)
        elif result.result == 'unsat':
            Instance.objects(filename=result.instance.filename).\
                update_one(set__num_unsat=cur_instance.num_unsat + 1)
        else:
            Instance.objects(filename=result.instance.filename).\
                update_one(set__num_unknown=cur_instance.num_unknown + 1)

    return data
