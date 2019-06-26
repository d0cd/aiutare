#!/usr/bin/env python3
import os
import sys
import subprocess
import signal
import datetime
import concurrent.futures


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
        process.wait(timeout=CONFIG["timeout"])
    # if it times out ...
    except subprocess.TimeoutExpired:
        # kill it
        # print('TIMED OUT:', repr(invocation), '... killing', process.pid, file=sys.stderr)
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        # set timeout result
        elapsed = CONFIG["timeout"]
        output = 'timeout (%.1f s)' % CONFIG["timeout"]
    # if it completes in time ...
    else:
        # measure run time
        end = datetime.datetime.now().timestamp()
        elapsed = end - start
        # get result
        stdout = process.stdout.read().decode("utf-8", "ignore")
        stderr = process.stderr.read().decode("utf-8", "ignore")
        output = stdout + stderr
    OUTPUT_HANDLERS[program](nickname, instance, output, elapsed, (INSTALL_PATH + CONFIG["schemas"]))


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


def bench(instances, handlers, config, install_path):
    global OUTPUT_HANDLERS
    OUTPUT_HANDLERS = handlers
    global CONFIG
    CONFIG = config
    global INSTALL_PATH
    INSTALL_PATH = install_path

    signal.signal(signal.SIGTERM, signal_handler)

    args = [[program, nickname, (INSTALL_PATH + command), instances] for
            program, specifications in CONFIG["commands"].items() for
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
