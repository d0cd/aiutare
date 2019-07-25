#!/usr/bin/env python3

import time
import psutil
import importlib.util
from pymongo import MongoClient
from subprocess import Popen, DEVNULL
from pathlib import Path


def write_config(config_filepath):

    spec = importlib.util.spec_from_file_location("config", config_filepath)
    config_file = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_file)
    config = config_file.config
    # Converts modules into importable format
    config["schemas"] = config["schemas"].rsplit(".", 1)[0].replace("/", ".")
    config["schemas"] = config["schemas"].rsplit(".", 1)[0].replace("\\", ".")
    for program, handler in config["handlers"].items():
        config["handlers"][program] = handler.rsplit(".", 1)[0].replace("/", ".")
        config["handlers"][program] = handler.rsplit(".", 1)[0].replace("\\", ".")

    # Writes a local copy of the user-provided config file
    with open(Path(r"bin/benching/config.py"), "w") as file:
        file.write("config = " + str(config) + "\n")
        file.flush()


def start_server(config_filepath):
    write_config(config_filepath)

    # Checks if a server is already running
    for process in psutil.process_iter():
        if process.name() == "mongod":
            return

    Popen(["mongod", "--dbpath", str(Path(r"./results")), "--logpath", str(Path(r"./results/log/mongodb.log")), " --replSet",
           "monitoring_replSet"], stdout=DEVNULL)

    # Waits until the server is accepting connections before exiting
    client = MongoClient()
    while client.local.command('ping')['ok'] != 1.0:
        time.sleep(0.5)


def end_server():
    for process in psutil.process_iter():
        if process.name() == "mongod":
            process.kill()
