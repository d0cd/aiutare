from subprocess import Popen
import psutil
from mongoengine import connect
from bin.config import config

Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
      " --replSet monitoring_replSet".split())

db1 = connect(config["database_name"], replicaset="monitoring_replSet")
db1.drop_database(config["database_name"])

procname = "mongod"

for proc in psutil.process_iter():
    if proc.name() == procname:
        proc.kill()
