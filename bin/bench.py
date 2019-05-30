#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import signal
import datetime
import concurrent.futures
import importlib
from importlib import util

from collections import namedtuple

# data
CSV_HEADER = "Instance,Result,Time\n"
RESULT = namedtuple('Result', ('problem', 'result', 'elapsed'))


def output2result(problem, output):
    # it's important to check for unsat first, since sat
    # is a substring of unsat
    if 'UNSAT' in output or 'unsat' in output:
        return 'unsat'
    if 'SAT' in output or 'sat' in output:
        return 'sat'
    if 'UNKNOWN' in output or 'unknown' in output:
        return 'unknown'

    print(problem, ': Couldn\'t parse output', file=sys.stderr)
    return 'error'


def run_problem(command, problem):
    # pass the problem to the command
    invocation = "%s %s" % (command, problem)
    # get start time
    start = datetime.datetime.now().timestamp()
    # run command
    process = subprocess.Popen(
        invocation,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    # wait for it to complete
    try:
        process.wait(timeout=CATEGORY.TIMEOUT)
    # if it times out ...
    except subprocess.TimeoutExpired:
        # kill it
        print('TIMED OUT:', repr(invocation), '... killing', process.pid, file=sys.stderr)
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        # set timeout result
        elapsed = CATEGORY.TIMEOUT
        output = 'timeout (%.1f s)' % CATEGORY.TIMEOUT
    # if it completes in time ...
    else:
        # measure run time
        end = datetime.datetime.now().timestamp()
        elapsed = end - start
        # get result
        stdout = process.stdout.read().decode("utf-8", "ignore")
        stderr = process.stderr.read().decode("utf-8", "ignore")
        output = output2result(problem, stdout + stderr)
    # make result
    result = RESULT(
        problem=problem.split("/", 2)[2],
        result=output,
        elapsed=elapsed
    )
    return result


def run_solver(args):
    solver = args[0]
    command = args[1]
    problems = args[2]
    filename = "results/%s/%s.csv" % (CATEGORY_NAME, solver)

    with open(filename, 'w+', buffering=1) as fp:
        fp.write(CSV_HEADER)
        for problem in problems:
            result = run_problem(command, problem)
            fp.write("%s,%s,%s\n" % (result.problem, result.result, result.elapsed))


def signal_handler():
    print("KILLING!")
    try:
        sys.exit(0)
    except SystemExit:
        exit(0)


def import_category():
    if len(sys.argv) != 2:
        print("Invalid Input. Usage:  python3 bench.py [category, e.g. sat]")
        exit(1)

    category_file = "bin/categories/%s.py" % sys.argv[1]
    if os.path.isfile(category_file):

        global CATEGORY_NAME
        CATEGORY_NAME = sys.argv[1]

        global CATEGORY
        spec = importlib.util.spec_from_file_location(CATEGORY_NAME, category_file)
        CATEGORY = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(CATEGORY)

    else:
        print("File at %s not found" % category_file)
        exit(1)


def main():
    import_category()

    signal.signal(signal.SIGTERM, signal_handler)
    problems = glob.glob("instances/%s/**/*.%s*" % (CATEGORY_NAME, CATEGORY.FILE_EXTENSION), recursive=True)
    print(len(problems))

    # Need to delete old result files to maintain consistency with currently specified solvers
    for filePath in glob.glob("results/%s/*.csv" % CATEGORY_NAME):
        os.remove(filePath)

    args = [[solver, command, problems] for solver, command in CATEGORY.SOLVERS.items()]
    try:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(run_solver, args)
    except KeyboardInterrupt:
        print('Interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            exit(0)


if __name__ == '__main__':
    main()
