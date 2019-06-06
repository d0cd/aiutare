from mongoengine import *


# MongoEngine schemas:
# ---------------------

class SMTInstance(Document):
    filename = StringField(required=True)


class SMTResult(Document):
    program = StringField(required=True)
    nickname = StringField()
    # command = StringField()
    # version = StringField()
    instance = ReferenceField(SMTInstance, required=True)
    result = StringField(required=True)
    elapsed = FloatField(required=True)
