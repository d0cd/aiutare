from mongoengine import *


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
