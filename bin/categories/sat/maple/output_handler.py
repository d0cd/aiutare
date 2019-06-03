import sys


# Parses the stdout + stderr output from running the problem
# and extracts useful information
def output_handler(fp, problem, output, elapsed):
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
        print(problem, ': Couldn\'t parse output', file=sys.stderr)

    write_results(fp, problem, result, elapsed)


# Formats and writes information to the database
def write_results(fp, problem, result, elapsed):
    fp.write("%s,%s,%s\n" % (problem.split("/", 2)[2], result, elapsed))
