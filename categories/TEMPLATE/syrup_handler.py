import os
import importlib
from bin.benching.config import config
from bin.benching.error_file_writer import write_error


# Parses the stdout + stderr output from running the problem
# and extracts useful information
def output_handler(nickname, instance, output, elapsed):
    result = 'error'
    results_dict = {}

    try:
        # Basic parsing for SAT and UNSAT TODO: may need modification for your particular program output
        if 'UNSAT' in output or 'unsat' in output:
            result = 'unsat'
        elif 'SAT' in output or 'sat' in output:
            result = 'sat'
        elif 'TIMEOUT' in output or 'timeout' in output:
            result = 'timeout'
        elif 'UNKNOWN' in output or 'unknown' in output:
            result = 'unknown'

        # TODO: add extra information from output to results_dict here if needed

    # Catches any errors in the user-made parsing above
    except Exception as e:

        write_error(nickname, instance, str(e))

    # Passes off info to the schemas file to be written to the database
    finally:
        schemas = importlib.import_module(config["schemas"])
        schemas.write_results(os.path.basename(__file__).rsplit("_", 1)[0],
                              nickname, instance, result, elapsed, results_dict)
