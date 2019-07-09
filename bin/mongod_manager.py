#!/usr/bin/env python3

import time
import psutil
from pymongo import MongoClient
from subprocess import Popen, DEVNULL


def start_server():
    # Checks if a server is already running
    for process in psutil.process_iter():
        if process.name() == "mongod":
            return

    Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
          " --replSet monitoring_replSet".split(), stdout=DEVNULL)

    # Waits until the server is accepting connections before exiting
    client = MongoClient()
    while client.local.command('ping')['ok'] != 1.0:
        time.sleep(0.5)


def end_server():
    for process in psutil.process_iter():
        if process.name() == "mongod":
            process.kill()
