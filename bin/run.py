import sys
import subprocess
from subprocess import Popen
from bin.parse_instances import parse_instances
from bin.bench import bench
from bin.analyze import analyze


def main():

    mongo_server = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split(),
                         stdout=subprocess.DEVNULL)

    num_bench = 1
    if len(sys.argv) > 1 and sys.argv[1] >= 0:  # running bench 0 times just calls analyze
        num_bench = sys.argv[1]

    if num_bench > 0:
        parse_instances()

        for _ in range(0, num_bench):
            bench()

    analyze()

    mongo_server.terminate()


if __name__ == '__main__':
    main()
