import os
import importlib
from bin.config import config
from bin.error_file_writer import write_error

# Parses the stdout + stderr output from running the problem
# and extracts useful information
def output_handler(nickname, instance, output, elapsed):
    result = 'error'
    results_dict = {}

    try:
        # Basic parsing for SAT and UNSAT
        if 'UNSAT' in output or 'unsat' in output:
            result = 'unsat'
        elif 'SAT' in output or 'sat' in output:
            result = 'sat'
        elif 'TIMEOUT' in output or 'timeout' in output:
            result = output
        elif 'UNKNOWN' in output or 'unknown' in output:
            result = 'unknown'

        # Advanced parsing for feature extraction
        if result == 'sat':
            output_string = output.replace(" ", "")

            names = ["num_variables", "num_clauses", "num_conflicts", "num_decisions", "num_propagations"]

            start_arr = ["Numberofvariables:", "Numberofclauses:", "Conflicts|", "Decisions|", "Propagations|"]

            end_arr = ["|", "|", "|", "|", "|"]

            for i in range(len(names)):
                index_start = output_string.rindex(start_arr[i]) + len(start_arr[i])
                index_end = index_start + output_string[index_start:].index(end_arr[i])
                results_dict[names[i]] = float(output_string[index_start:index_end])

    # Catches any errors in the user-made parsing above
    except (TypeError, NameError, ValueError, IndexError) as e:
        write_error(nickname, instance, e)
    # Passes off info to the schemas file to be written to the database
    finally:
        schemas = importlib.import_module(config["schemas"])
        schemas.write_results(os.path.basename(__file__).rsplit("_", 1)[0],
                              nickname, instance, result, elapsed, results_dict)
