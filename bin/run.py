#!/usr/bin/env python3

import sys
import subprocess
import json
from subprocess import Popen
from bin.parse_instances import parse_instances
from bin.bench import bench
from bin.analyze import analyze


def main():

    config = json.loads(open(sys.argv[1], 'r').read())
    with open("bin/config.py", "w") as file:
        file.write("config = " + str(config))

    mongo_server = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split(),
                         stdout=subprocess.DEVNULL)

    num_bench = 1
    if len(sys.argv) > 2 and int(sys.argv[2]) >= 0:  # running bench 0 times just calls analyze
        num_bench = int(sys.argv[2])

    if num_bench > 0:

        # TODO: possibly move parse_instances here since they're only read once per run call
        parse_instances()

        for _ in range(0, num_bench):
            bench()

    analyze()

    mongo_server.terminate()


if __name__ == '__main__':
    main()
