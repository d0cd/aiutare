#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import signal
import datetime
import concurrent.futures
import json
import importlib
from importlib import util

from collections import namedtuple

# data
CSV_HEADER = "Instance,Result,Time\n"
RESULT = namedtuple('Result', ('problem', 'result', 'elapsed'))


def run_problem(program, command, problem):
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
        process.wait(timeout=TIMEOUT)
    # if it times out ...
    except subprocess.TimeoutExpired:
        # kill it
        print('TIMED OUT:', repr(invocation), '... killing', process.pid, file=sys.stderr)
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        # set timeout result
        elapsed = TIMEOUT
        output = 'timeout (%.1f s)' % TIMEOUT
    # if it completes in time ...
    else:
        # measure run time
        end = datetime.datetime.now().timestamp()
        elapsed = end - start
        # get result
        stdout = process.stdout.read().decode("utf-8", "ignore")
        stderr = process.stderr.read().decode("utf-8", "ignore")
        output = OUTPUT_HANDLERS[program](problem, stdout + stderr)
    # make result
    result = RESULT(
        problem=problem.split("/", 2)[2],
        result=output,
        elapsed=elapsed
    )
    return result


# program, specification["id"], specification["command"], problems
def run_solver(args):
    program = args[0]
    nickname = args[1]
    command = args[2]
    problems = args[3]
    filename = "results/%s/%s.csv" % (CATEGORY_NAME, nickname)

    with open(filename, 'w+', buffering=1) as fp:
        fp.write(CSV_HEADER)
        for problem in problems:
            result = run_problem(program, command, problem)
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

    global CATEGORY_NAME
    CATEGORY_NAME = sys.argv[1]

    run_file = "bin/categories/%s/run_%s.json" % (CATEGORY_NAME, CATEGORY_NAME)
    if os.path.isfile(run_file):

        with open(run_file) as f:
            json_data = json.load(f)

            global FILE_EXTENSION
            FILE_EXTENSION = json_data["FILE_EXTENSION"]
            global TIMEOUT
            TIMEOUT = json_data["TIMEOUT"]
            global PROGRAMS
            PROGRAMS = json_data["PROGRAMS"]

        global OUTPUT_HANDLERS
        OUTPUT_HANDLERS = {}

        for program_dir in os.listdir("bin/categories/%s" % CATEGORY_NAME):
            if os.path.isdir("bin/categories/%s/%s" % (CATEGORY_NAME, program_dir)):
                spec = importlib.util.spec_from_file_location("output2result",
                                                              "bin/categories/%s/%s/output2result.py" %
                                                              (CATEGORY_NAME, program_dir))
                new_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(new_module)

                OUTPUT_HANDLERS[program_dir] = new_module.output2result

    else:
        print("File at %s not found" % run_file)
        exit(1)


def main():
    import_category()

    signal.signal(signal.SIGTERM, signal_handler)
    problems = glob.glob("instances/%s/**/*.%s*" % (CATEGORY_NAME, FILE_EXTENSION), recursive=True)
    print("%d problem(s) found" % len(problems))

    # Need to delete old result files to maintain consistency with currently specified solvers
    for filePath in glob.glob("results/%s/*.csv" % CATEGORY_NAME):
        os.remove(filePath)

    args = [[program, nickname, command, problems] for program, specifications in PROGRAMS.items() for
            nickname, command in specifications.items()]
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
