#!/usr/bin/env python3

import sys
import json
import glob
import mongoengine
import importlib
from subprocess import Popen, DEVNULL
from multiprocessing import Process


def write_config(config):

    # convert modules into importable format
    config["schemas"] = config["schemas"].rsplit(".", 1)[0].replace("/", ".")
    for program, handler in config["handlers"].items():
        config["handlers"][program] = handler.rsplit(".", 1)[0].replace("/", ".")

    with open("bin/config.py", "w") as file:
        file.write("config = " + str(config) + "\n")
        file.flush()


def write_instances(config, instances):
    schemas = importlib.import_module(config["schemas"])

    mongoengine.connect(config["database_name"])

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not schemas.Instance.objects(filename=stripped_instance):
            schemas.Instance.objects(filename=stripped_instance).\
                update_one(upsert=True, set__filename=stripped_instance)

    mongoengine.connection.disconnect()


def collect_handlers(config):

    handlers = {}

    for program in config["handlers"].items():
        cur_module = importlib.import_module(program[1])
        handlers[program[0]] = cur_module.output_handler

    return handlers


def main():

    config = json.loads(open(sys.argv[1], 'r').read())
    write_config(config)

    mongo_server = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split(),
                         stdout=DEVNULL)

    num_bench = 1
    if len(sys.argv) > 2 and int(sys.argv[2]) >= 0:  # running bench 0 times just calls analyze
        num_bench = int(sys.argv[2])

    if num_bench != 0:

        instances = glob.glob("%s/**/*.*" % config["instances"], recursive=True)
        print("%d instance(s) found" % len(instances))

        p = Process(target=write_instances, args=(config, instances))
        p.start()
        handlers = collect_handlers(config)
        p.join()

        from bin.bench import bench
        for _ in range(0, num_bench):
            bench(instances, handlers)

    from bin.analyze import analyze
    analyze()

    mongo_server.terminate()


if __name__ == '__main__':
    main()
