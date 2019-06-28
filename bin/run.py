#!/usr/bin/env python3
import errno
import glob
import sys
import time
import progressbar
import mongoengine
import importlib.util
import subprocess
from pymongo import MongoClient
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

    code = 1
    while not code == 0:
        code = subprocess.run("mongo --eval 'rs.initiate()'".split(),
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        time.sleep(.5)

    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

    for instance in instances:
        stripped_instance = instance.split("/", 1)[1]

        if not schemas.Instance.objects(filename=stripped_instance):
            schemas.Instance.objects(filename=stripped_instance). \
                update_one(upsert=True, set__filename=stripped_instance)

    mongoengine.connection.disconnect()


def collect_handlers(config):
    handlers = {}

    for program in config["handlers"].items():
        cur_module = importlib.import_module(program[1])
        handlers[program[0]] = cur_module.output_handler

    return handlers


def monitor_database(config, num_instances, num_bench):
    commands = config["commands"]

    num_commands = 0
    for program in list(commands.values()):
        num_commands += len(list(program.values()))

    print("Running %d total commands\n" % (num_commands * num_instances * num_bench))

    client = MongoClient()
    db = client[config["database_name"]]

    with db.watch([{'$match': {'operationType': 'insert'}}]) as stream:

        for _ in progressbar.progressbar(range(num_commands * num_instances * num_bench)):
            stream.next()
            # print(stream.next()["fullDocument"])  TODO: possibly use for live-updating output


def create_error_file():
    with open("bin/errors.txt", "w") as f:
        try:
            f.write("Errors:0\n")
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise


def main(config_filepath, num_bench):
    spec = importlib.util.spec_from_file_location("config", config_filepath)
    config_file = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_file)
    config = config_file.config

    write_config(config)

    create_error_file()

    # install_path = config_filepath[:config_filepath.rindex("/aiutare/")+9]

    mongod = subprocess.Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
                              " --replSet monitoring_replSet".split(), stdout=subprocess.DEVNULL)

    if num_bench > 0:

        instances = glob.glob("%s/**/*.%s" % (config["instances"], config["file_extension"]), recursive=True)

        instance_writer = Process(target=write_instances, args=(config, instances))
        instance_writer.start()
        handlers = collect_handlers(config)
        instance_writer.join()

        database_monitor = Process(target=monitor_database, args=(config, len(instances), num_bench))
        database_monitor.start()

        from bin.bench import bench
        for _ in range(0, num_bench):
            try:
                bench(instances, handlers)
            except Exception as e:
                print("KILLING BENCHMARKING: ", e, file=sys.stderr)

        database_monitor.terminate()

        from bin.error_file_writer import read_num_errors
        read_num_errors()

    from bin.analyze import analyze
    analyze()

    mongod.terminate()


if __name__ == '__main__':
    main(config_filepath=sys.argv[1], num_bench=1)
