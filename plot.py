#!/usr/bin/env python3
import sys
import argparse
from bin.plotting.test_scatterplot import scatterplot
from bin.plotting.test_3Dgrapher import scatterplot_3d
from bin.mongod_manager import start_server, end_server


def main():
    # TODO: parse all args here using argparse
    config_filepath = sys.argv[1]

    start_server(config_filepath)

    scatterplot()
    scatterplot_3d()

    kill_server = False  # TODO: handle with argparse
    if kill_server:
        end_server()


if __name__ == '__main__':
    main()
