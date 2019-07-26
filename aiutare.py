#!/usr/bin/env python3

import sys
import argparse
from bin.benching.run import run
from bin.analyze import analyze
from bin.mongod_manager import write_config, start_server, end_server


def parse_arguments():
    # create arg parser
    global_parser = argparse.ArgumentParser(description='modular benchmarking framework')

    # global args
    global_parser.add_argument(
        '-cfg',
        dest='config_filepath',
        type=str,
        default=None,
        help='absolute filepath to the user-provided config file (default: uses config provided to setup.py'
    )
    global_parser.add_argument(
        '-n',
        '--num-runs',
        dest='num_runs',
        type=int,
        default=1,
        help='Number of times to run all solvers on all problem instances (default: 1)'
    )
    global_parser.add_argument(
        '-ks',
        '--kill-server',
        dest='kill_server',
        action='store_true',
        default=False,
        help='Kill MongoDB server process before exiting program (default: False)'
    )

    return global_parser.parse_args()


def main():
    args = parse_arguments()

    if args.config_filepath is not None:
        write_config(args.config_filepath)

    start_server()

    if args.num_runs > 0:
        run(args.num_runs)
    analyze()

    if args.kill_server is True:
        end_server()


if __name__ == '__main__':
    main()