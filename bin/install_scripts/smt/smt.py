import sys


FILE_EXTENSION = "smt2"
TIMEOUT = 30.0

# The command line timeout values specified below should be 110% of the TIMEOUT value above
SOLVERS = {
    "CVC4": "tools/smt/cvc4 --lang smt --strings-exp --tlimit=33000 -q",
    "Z3":   "tools/smt/z3 -T:33",
}


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
