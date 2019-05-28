#!/usr/bin/env python3
import sys


PROBLEMS = "instances/smt/**/*.smt2*"
RESULTS_DIR = "results/smt"
SOLVERS = {
    "CVC4": ["tools/smt/cvc4 --lang smt --strings-exp --tlimit=33000 -q", 30.0],
    "Z3":   ["tools/smt/z3 -T:33", 30.0],
}


# Cannot be handled by helpers.py due to unique output from each problem type
def output2result(problem, output):
    # it's important to check for unsat first, since sat
    # is a substring of unsat
    if 'UNSAT' in output or 'unsat' in output:
        return 'unsat'
    if 'SAT' in output or 'sat' in output:
        return 'sat'
    if 'UNKNOWN' in output or 'unknown' in output:
        return 'unknown'

    # print(problem, ': Couldn\'t parse output', file=sys.stderr)
    return 'error'
