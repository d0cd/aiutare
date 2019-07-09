#!/usr/bin/env python3
import importlib
import mongoengine
import shutil
from subprocess import Popen, DEVNULL
from bin.benching.run import run
from bin.benching.config import config as og_config
from bin.verification.v_config import v_config
from categories.smt.schemas import Result, Instance


def modify_instance(nickname, filename, model):
    new_filename = v_config["instances"] + "/" + filename.rsplit('.', 1)[0] + "-" + nickname + ".smt2"
    shutil.copy(filename, new_filename)

    with open(new_filename, 'a') as v_inst:
        v_inst.write('\n')
        v_inst.write(model)


# Populate bin/verification/v_instances with new instances
# created by inserting solvers' models into original instances
def generate_v_instances():
    mongoengine.connect(og_config["database_name"], replicaset="monitoring_replSet")

    all_results = Result.objects()

    for sat_result in all_results:  # TODO: this is being skipped over
        if sat_result.result == "sat":
            modify_instance(sat_result.nickname, sat_result.instance.filename, sat_result.model)

    mongoengine.connection.disconnect()


def main():
    mongod = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
                   " --replSet monitoring_replSet".split(), stdout=DEVNULL)

    try:
        v_db = mongoengine.connect(v_config["database_name"], replicaset="monitoring_replSet")
        v_db.drop_database(v_config["database_name"])

        generate_v_instances()

        # run("bin/verification/v_config.py", 1)

    except Exception as e:
        mongod.terminate()
        print(e)


if __name__ == '__main__':
    main()
