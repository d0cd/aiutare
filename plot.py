#!/usr/bin/env python3

import argparse
from bin.plotting.test_scatterplot import scatterplot
from bin.plotting.test_3Dgrapher import scatterplot_3d
from bin.mongod_manager import start_server, end_server


def main():
    # TODO: parse all args here using argparse

    start_server()

    scatterplot()
    # scatterplot_3d()

    kill_server = False  # TODO: handle with argparse
    if kill_server:
        end_server()


if __name__ == '__main__':
    main()
