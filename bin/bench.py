#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import signal
import datetime
import concurrent.futures
import importlib

from collections import namedtuple

# data
CSV_HEADER = "Instance,Result,Time\n"
RESULT = namedtuple('Result', ('problem', 'result', 'elapsed'))

# constants
ERROR_RESULT = 'error'


def run_problem(command, timeout, problem):
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
        process.wait(timeout=timeout)
    # if it times out ...
    except subprocess.TimeoutExpired:
        # kill it
        print('TIMED OUT:', repr(invocation), '... killing', process.pid, file=sys.stderr)
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        # set timeout result
        elapsed = timeout
        output = 'timeout (%.1f s)' % timeout
    # if it completes in time ...
    else:
        # measure run time
        end = datetime.datetime.now().timestamp()
        elapsed = end - start
        # get result
        stdout = process.stdout.read().decode("utf-8", "ignore")
        stderr = process.stderr.read().decode("utf-8", "ignore")
        output = CATEGORY.output2result(problem, stdout + stderr)
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
    timeout = args[2]
    problems = args[3]
    filename = "%s/%s.csv" % (CATEGORY.RESULTS_DIR, solver)

    with open(filename, 'w+', buffering=1) as fp:
        fp.write(CSV_HEADER)
        for problem in problems:
            result = run_problem(command, timeout, problem)
            fp.write("%s,%s,%s\n" % (result.problem, result.result, result.elapsed))


def signal_handler():
    print("KILLING!")
    try:
        sys.exit(0)
    except SystemExit:
        exit(0)


# TODO: eventually handle JSON reading to set SOLVERS here
def import_category():
    if len(sys.argv) != 2:
        print("Invalid Input. Usage:  python3 bench.py [category, e.g. sat]")
        exit(1)

    category_file = "bin/%s.py" % sys.argv[1]
    if os.path.isfile(category_file):
        global CATEGORY
        CATEGORY = importlib.import_module(sys.argv[1])
    else:
        print("File at %s not found" % category_file)
        exit(1)


def main():
    import_category()

    signal.signal(signal.SIGTERM, signal_handler)
    problems = glob.glob(CATEGORY.PROBLEMS, recursive=True)
    print(len(problems))

    # Need to delete old result files to maintain consistency with currently specified solvers
    for filePath in glob.glob("%s/*.csv" % CATEGORY.RESULTS_DIR):
        os.remove(filePath)

    args = [[solver, command[0], command[1], problems] for solver, command in CATEGORY.SOLVERS.items()]
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
