import os
import sys
import json
import importlib
from importlib import util

CONFIG = json.loads(open("bin/config.json", 'r').read())
spec = importlib.util.spec_from_file_location("schemas", CONFIG["schemas"])
schemas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas)


# Parses the stdout + stderr output from running the problem
# and extracts useful information
def output_handler(nickname, instance, output, elapsed):
    result = 'error'

    # TODO: Fill in the statements below to extract needed information from program output
    if 'unsat' in output:
        result = 'unsat'
    elif 'sat' in output:
        result = 'sat'
    elif 'timeout' in output:
        result = output
    elif 'unknown' in output:
        result = 'unknown'
    
    model = find_model(output)

    schemas.write_results(os.path.basename(__file__).rsplit("_", 1)[0], nickname, instance, result, elapsed, output, model)


def find_model(output):
    start = output.find( '(model' )

    if start == -1:
        return ""

    count  = 1
    pos    = start
    result = ""

    while count > 0 and pos < len(output):
        result += output[pos]
        if output[pos] == "(":
            count += 1
        if output[pos] == ")":
            count -= 1

    result += output[pos]

    return result