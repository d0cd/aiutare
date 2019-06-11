import glob
import json
import importlib
from importlib import util
import mongoengine


CONFIG = json.loads(open("bin/config.json", 'r').read())


def main():
    instances = glob.glob("%s/**/*.*" % CONFIG["instances"], recursive=True)
    print("%d instance(s) found" % len(instances))

    spec = importlib.util.spec_from_file_location("schemas", CONFIG["schemas"])
    schemas = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schemas)

    # Parses all unique instances and writes them to the database
    mongoengine.connect(CONFIG["database_name"])

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not schemas.Instance.objects(filename=stripped_instance):
            schemas.Instance.objects(filename=stripped_instance).\
                update_one(upsert=True, set__filename=stripped_instance,
                           set__num_sat=0, set__num_unsat=0, set__num_unknown=0,)

    mongoengine.connection.disconnect()

    # Writes the instances to a local file to be read repeatedly by bench.py
    with open("bin/written_instances.json", 'w') as written_instances:
        written_instances.write(json.dumps(instances))


if __name__ == '__main__':
    main()