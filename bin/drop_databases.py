#!/usr/bin/env python3
from subprocess import Popen
from mongoengine import connect
from bin.config import config

mongod = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
               " --replSet monitoring_replSet".split())

db1 = connect(config["database_name"], replicaset="monitoring_replSet")
db1.drop_database(config["database_name"])

print("Database '%s' successfully dropped" % config["database_name"])

mongod.terminate()
