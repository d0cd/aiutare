#!/usr/bin/env python3
import os
import mongoengine
import shutil
# from bin.benching.run import run
from bin.benching.config import config as og_config
from bin.verification.v_config import v_config
from categories.smt.schemas import Result  # , Instance
from bin.mongod_manager import start_server, end_server


def parse_models(models):
    models_arr = models.replace('\n', '').split("(model")[1:]

    vars_and_values = []

    for i in range(len(models_arr)):
        vars_and_values.append([])
        statements = models_arr[i].split("(define-fun ")[1:]
        for statement in statements:
            var = statement[0:statement.index(" ()")]
            value = statement[statement.find('"') + 1:statement.rfind('"')]
            vars_and_values[i].append((var, value))

    return vars_and_values


def format_clauses(vars_and_values):
    formatted_clauses = []

    for variable_set in vars_and_values:
        clauses_string = ""
        for var_data in variable_set:
            new_clause = "(assert (= %s \"%s\"))\n" % (var_data[0], var_data[1])
            clauses_string += new_clause
        formatted_clauses.append(clauses_string)

    return formatted_clauses


def insert_statements(new_filename, formatted_clauses):
    with open(new_filename, 'r+') as v_inst:
        cur_check_sat = 0
        for line in v_inst:
            if line == "(check-sat)":
                v_inst.write(formatted_clauses[cur_check_sat])
                cur_check_sat += 1


def modify_instance(nickname, filename, models):
    new_dir = v_config["instances"] + "/" + nickname
    new_filename = new_dir + "/" + filename.rsplit('/', 1)[1]

    vars_and_values = parse_models(models)
    formatted_clauses = format_clauses(vars_and_values)

    try:
        shutil.copy(filename, new_filename)

    except FileNotFoundError:
        os.makedirs(new_dir, exist_ok=True)
        shutil.copy(filename, new_filename)

    finally:
        insert_statements(new_filename, formatted_clauses)


# Populate bin/verification/v_instances with new instances
# created by inserting solvers' models into original instances
def generate_v_instances():
    mongoengine.connect(og_config["database_name"], replicaset="monitoring_replSet")

    # TODO: should also probably delete all files in v_instances

    for sat_result in Result.objects():
        if sat_result.result == "sat":
            modify_instance(sat_result.nickname, sat_result.instance.filename, sat_result.model)

    mongoengine.connection.disconnect()


def main():
    start_server()

    try:
        generate_v_instances()

        v_db = mongoengine.connect(v_config["database_name"], replicaset="monitoring_replSet")
        v_db.drop_database(v_config["database_name"])
        v_db.close()

        # run("bin/verification/v_config.py", 1)

    except Exception as e:
        print(e)

    finally:
        kill_server = False  # TODO: handle with argparse
        if kill_server:
            end_server()


if __name__ == '__main__':
    main()
