import glob
import json
import importlib
from importlib import util
import mongoengine
from bin.config import config


def parse_instances():
    instances = glob.glob("%s/**/*.*" % config["instances"], recursive=True)
    print("%d instance(s) found" % len(instances))

    spec = importlib.util.spec_from_file_location("schemas", config["schemas"])
    schemas = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schemas)

    # Parses all unique instances and writes them to the database
    mongoengine.connect(config["database_name"])

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not schemas.Instance.objects(filename=stripped_instance):
            schemas.Instance.objects(filename=stripped_instance).\
                update_one(upsert=True, set__filename=stripped_instance)

    mongoengine.connection.disconnect()

    # Writes the instances to a local file to be read repeatedly by bench.py
    with open("bin/written_instances.json", 'w') as written_instances:
        written_instances.write(json.dumps(instances))
