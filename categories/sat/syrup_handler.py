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
    # else:
    #     print(instance, ': Couldn\'t parse output', file=sys.stderr)

    results_dict = {}

    if result == 'sat':
        output_string = output.replace(" ", "")

        names = ["num_variables", "num_clauses", "num_conflicts", "num_decisions", "num_propagations"]

        start_arr = ["Numberofvariables:", "Numberofclauses:", "Conflicts|", "Decisions|", "Propagations|"]

        end_arr = ["|", "|", "|", "|", "|"]

        for i in range(len(names)):
            index_start = output_string.index(start_arr[i]) + len(start_arr[i])
            index_end = index_start + output_string[index_start:].index(end_arr[i])
            results_dict[names[i]] = float(output_string[index_start:index_end])

    schemas = importlib.import_module(config["schemas"])
    schemas.write_results(os.path.basename(__file__).rsplit("_", 1)[0],
                          nickname, instance, result, elapsed, results_dict)
