import json
from mongoengine import connect


CONFIG = json.loads(open("bin/config.json", 'r').read())

db1 = connect(CONFIG["database_name"])
db1.drop_database(CONFIG["database_name"])
