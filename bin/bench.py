#!/usr/bin/env python3
import os
import sys
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


def run_problem(program, nickname, command, instance):
    # pass the problem to the command
    invocation = "%s %s" % (command, instance)
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
        output = stdout + stderr
    OUTPUT_HANDLERS[program](nickname, instance, output, elapsed)


# program, specification["id"], specification["command"], problems
def run_solver(args):
    program = args[0]
    nickname = args[1]
    command = args[2]
    instances = args[3]

    for instance in instances:
        run_problem(program, nickname, command, instance)


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
            if os.path.isdir("bin/categories/%s/%s" % (CATEGORY_NAME, program_dir)) and program_dir != "__pycache__":
                spec = importlib.util.spec_from_file_location("output_handler",
                                                              "bin/categories/%s/%s/output_handler.py" %
                                                              (CATEGORY_NAME, program_dir))
                new_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(new_module)

                OUTPUT_HANDLERS[program_dir] = new_module.output_handler

    else:
        print("Run file at %s not found" % run_file)
        exit(1)


def main():
    import_category()

    signal.signal(signal.SIGTERM, signal_handler)

    written_instances = open("bin/written_instances.json", 'r').read()
    instances = json.loads(written_instances)

    args = [[program, nickname, command, instances] for program, specifications in PROGRAMS.items() for
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
