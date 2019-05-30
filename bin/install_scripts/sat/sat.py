import sys


FILE_EXTENSION = "cnf"
TIMEOUT = 30.0

# The command line timeout values specified below should be 110% of the TIMEOUT value above
SOLVERS = {
    "syrup":    "tools/sat/syrup/syrup/bin/glucose-syrup -nthreads=8 -model -maxmemory=50000 -cpu-lim=33",
    "minisat":  "minisat -cpu-lim=33",
    "maple":    "tools/sat/maple/MapleLRB_LCMoccRestart/sources/simp/glucose_static -cpu-lim=33",
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
