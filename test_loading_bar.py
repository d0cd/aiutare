#!/usr/bin/env python3
from subprocess import run, Popen, DEVNULL
import setuptools
import platform
import time
import psutil


Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
      " --replSet monitoring_replSet".split(), stdout=DEVNULL)

good_connect = False
while not good_connect:
    output = run("mongo --eval 'rs.initiate()'".split(), stdout=DEVNULL).stderr
    print(output)
    time.sleep(1)


PROCNAME = "mongod"

for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        proc.kill()
