import sys


def output2result(problem, output):
    # check for unsat first, since sat is a substring of unsat
    if 'UNSAT' in output or 'unsat' in output:
        return 'unsat'
    if 'SAT' in output or 'sat' in output:
        return 'sat'
    if 'UNKNOWN' in output or 'unknown' in output:
        return 'unknown'

    print(problem, ': Couldn\'t parse output', file=sys.stderr)
    return 'error'
