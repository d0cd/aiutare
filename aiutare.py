#!/usr/bin/env python3

import sys
import argparse
from subprocess import Popen, DEVNULL
from bin.benching.run import run


def main():
    # TODO: parse all args here using argparse
    config_filepath = sys.argv[1]
    num_bench = 1
    if len(sys.argv) > 2:
        num_bench = int(sys.argv[2])

    mongod = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
                   " --replSet monitoring_replSet".split(), stdout=DEVNULL)

    run(config_filepath, num_bench)

    mongod.terminate()


if __name__ == '__main__':
    main()
