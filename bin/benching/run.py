#!/usr/bin/env python3
import glob
import sys
import time
import progressbar
import importlib.util
import subprocess
from pymongo import MongoClient
from multiprocessing import Process
from bin.benching.error_file_writer import read_num_errors, create_error_file


def write_config(config):
    # convert modules into importable format
    config["schemas"] = config["schemas"].rsplit(".", 1)[0].replace("/", ".")
    for program, handler in config["handlers"].items():
        config["handlers"][program] = handler.rsplit(".", 1)[0].replace("/", ".")

    with open("bin/benching/config.py", "w") as file:
        file.write("config = " + str(config) + "\n")
        file.flush()


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

    code = 1
    while not code == 0:  # Retry connecting to database until it is setup TODO: replace with pymongo.ping
        code = subprocess.run("mongo --eval 'rs.initiate()'".split(),
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        time.sleep(.5)

    if num_bench > 0:

        create_error_file()

        instances = glob.glob("%s/**/*.%s" % (config["instances"], config["file_extension"]), recursive=True)

        schemas = importlib.import_module(config["schemas"])
        instance_writer = Process(target=schemas.write_instances, args=[instances])
        instance_writer.start()
        handlers = collect_handlers(config)
        instance_writer.join()

        database_monitor = Process(target=monitor_database, args=(config, len(instances), num_bench))
        database_monitor.start()

        from bin.benching.bench import bench
        for _ in range(0, num_bench):
            try:
                bench(instances, handlers)
            except Exception as e:
                print("KILLING BENCHMARKING: ", e, file=sys.stderr)

        database_monitor.terminate()

        read_num_errors()

    from bin.analyze import analyze
    analyze()
