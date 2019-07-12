#!/usr/bin/env python3
import os
import mongoengine
import shutil
from multiprocessing import Process
from bin.benching.run import run
from bin.benching.config import config as og_config
from bin.verification.v_config import config as v_config
from categories.smt.schemas import Result  # , Instance
from bin.mongod_manager import start_server, end_server


def parse_models(models):
    models_arr = models.replace('\n', '').split("(model")[1:]
    assertions = []

    for model in models_arr:
        model = model[0:-1]
        model = model.replace("() String", "")

        lines = model.split("(define-fun")[1:]
        for i in range(len(lines)):
            lines[i] = "(assert (= " + lines[i].strip() + ")"

        assertions.append("\n" + '\n'.join(lines) + "\n")

    return assertions


def insert_statements(new_filename, assertions):
    with open(new_filename, 'r+') as v_inst:

        lines = v_inst.readlines()
        cur_check_sat = 0
        for i in range(len(lines)):
            if "(check-sat)" in lines[i]:
                lines[i] = assertions[cur_check_sat] + "\n" + lines[i]
                cur_check_sat += 1

        v_inst.seek(0)
        v_inst.truncate()
        v_inst.writelines(lines)


def modify_instance(nickname, filename, models):
    new_dir = v_config["instances"] + "/" + nickname
    new_filename = new_dir + "/" + filename.rsplit('/', 1)[1]

    assertions = parse_models(models)

    try:
        shutil.copy(filename, new_filename)

    except FileNotFoundError:
        os.makedirs(new_dir, exist_ok=True)
        shutil.copy(filename, new_filename)

    finally:
        insert_statements(new_filename, assertions)


# Populate bin/verification/v_instances with new instances
# created by inserting solvers' models into original instances
def generate_v_instances():
    mongoengine.connect(og_config["database_name"], replicaset="monitoring_replSet")

    # Clear the v_instances directory for each program run
    shutil.rmtree(v_config["instances"], ignore_errors=True)
    os.mkdir(v_config["instances"])

    for sat_result in Result.objects():
        if sat_result.result == "sat":
            modify_instance(sat_result.nickname, sat_result.instance.filename, sat_result.model)

    mongoengine.connection.disconnect()


def drop_v_db(db_name):
    v_db = mongoengine.connect(db_name, replicaset="monitoring_replSet")
    v_db.drop_database(db_name)
    v_db.close()


def main():
    start_server()

    instance_generator = Process(target=generate_v_instances)
    v_db_dropper = Process(target=drop_v_db, args=[v_config["database_name"]])
    instance_generator.start()
    instance_generator.join()
    v_db_dropper.start()
    v_db_dropper.join()

    run("bin/verification/v_config.py", 1)

    kill_server = False  # TODO: handle with argparse
    if kill_server:
        end_server()


if __name__ == '__main__':
    main()
