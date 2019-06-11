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

    if 'UNSAT' in output or 'unsat' in output:
        result = 'unsat'
    elif 'SAT' in output or 'sat' in output:
        result = 'sat'
    elif 'TIMEOUT' in output or 'timeout' in output:
        result = output
    elif 'UNKNOWN' in output or 'unknown' in output:
        result = 'unknown'
    else:
        print(instance, ': Couldn\'t parse output', file=sys.stderr)

    schemas.write_results(os.path.basename(__file__).rsplit("_", 1)[0], nickname, instance, result, elapsed)
