#!/usr/bin/env python3
import glob
import progressbar
import mongoengine
import importlib.util
import psutil
from pymongo import MongoClient
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

    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")

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


def run(config_filepath, num_bench):

    spec = importlib.util.spec_from_file_location("config", config_filepath)
    config_file = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_file)
    config = config_file.config

    write_config(config)

    # install_path = config_filepath[:config_filepath.rindex("/aiutare/")+9]

    Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
          " --replSet monitoring_replSet".split(), stdout=DEVNULL)

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
            bench(instances, handlers)

    from bin.analyze import analyze
    analyze()

    procname = "mongod"

    for proc in psutil.process_iter():
        if proc.name() == procname:
            proc.kill()
