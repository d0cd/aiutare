#!/usr/bin/env python3
import sys


PROBLEMS = "instances/sat/**/*.cnf*"
RESULTS_DIR = "results/sat"
SOLVERS = {
    "syrup":    ["tools/sat/syrup/syrup/bin/glucose-syrup -nthreads=8 -model -maxmemory=50000 -cpu-lim=33", 30.0],
    "minisat":  ["minisat -cpu-lim=33", 30.0],
}


def output2result(problem, output):
    # it's important to check for unsat first, since sat
    # is a substring of unsat
    if 'UNSATISFIABLE' in output:   # Category specific
        return 'unsat'
    if 'SATISFIABLE' in output:     # Category specific
        return 'sat'
    if 'UNKNOWN' in output:         # Category specific
        return 'unknown'

    print(problem, ': Couldn\'t parse output', file=sys.stderr)
    return 'error'
