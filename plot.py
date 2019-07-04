#!/usr/bin/env python3

import argparse
from subprocess import Popen, DEVNULL
from bin.plotting.test_scatterplot import scatterplot
from bin.plotting.test_3Dgrapher import scatterplot_3d


def main():
    # TODO: parse all args here using argparse

    mongod = Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
                   " --replSet monitoring_replSet".split(), stdout=DEVNULL)

    scatterplot()
    # scatterplot_3d()

    mongod.terminate()


if __name__ == '__main__':
    main()
