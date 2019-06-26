import os
import sys
import importlib
from bin.config import config


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

    schemas = importlib.import_module(config["schemas"])
    schemas.write_results(os.path.basename(__file__).rsplit("_", 1)[0], nickname, instance, result, elapsed)
