#!/usr/bin/env python3

import sys
import argparse
from bin.benching.run import run
from bin.analyze import analyze
from bin.mongod_manager import start_server, end_server


def main():
    # TODO: parse all args here using argparse
    config_filepath = sys.argv[1]
    num_bench = 1
    if len(sys.argv) > 2:
        num_bench = int(sys.argv[2])

    start_server()

    run(config_filepath, num_bench)
    analyze()

    kill_server = False  # TODO: handle with argparse
    if kill_server:
        end_server()


if __name__ == '__main__':
    main()
