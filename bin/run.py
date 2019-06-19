#!/usr/bin/env python3

import sys
import json
import glob
import mongoengine
import importlib.util
from subprocess import Popen, DEVNULL

from bin.bench import bench
from bin.analyze import analyze


def parse_instances(config):
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


def main():

    config = json.loads(open(sys.argv[1], 'r').read())
    with open("bin/config.py", "w") as file:
        file.write("config = " + str(config))

    mongo_server = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split(),
                         stdout=DEVNULL)

    num_bench = 1
    if len(sys.argv) > 2 and int(sys.argv[2]) >= 0:  # running bench 0 times just calls analyze
        num_bench = int(sys.argv[2])

    if num_bench > 0:

        parse_instances(config)

        for _ in range(0, num_bench):
            bench()

    analyze()

    mongo_server.terminate()


if __name__ == '__main__':
    main()
