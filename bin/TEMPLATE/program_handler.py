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
    # if 'unsat' in output:
    #     result = 'unsat'
    # elif 'sat' in output:
    #     result = 'sat'
    # elif 'timeout' in output:
    #     result = output
    # elif 'unknown' in output:
    #     result = 'unknown'
    #
    # else:
    #     print(instance, ': Couldn\'t parse output', file=sys.stderr)

    schemas.write_results(os.path.basename(__file__).rsplit("_", 1)[0], nickname, instance, result, elapsed)
