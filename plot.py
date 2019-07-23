#!/usr/bin/env python3
import argparse
from bin.plotting.scatterplot import scatterplot
from bin.mongod_manager import start_server, end_server


def parse_arguments():
    # create arg parser
    global_parser = argparse.ArgumentParser(description='modular benchmarking framework')

    # global args
    global_parser.add_argument(
        metavar='config',
        dest='config_filepath',
        type=str,
        help='absolute filepath to the user-provided config file'
    )
    global_parser.add_argument(
        metavar='x',
        dest='x',
        type=str,
        help='Variable for the X axis'
    )
    global_parser.add_argument(
        metavar='y',
        dest='y',
        type=str,
        default=None,
        help='Variable for the Y axis'
    )
    global_parser.add_argument(
        '-z',
        dest='z',
        type=str,
        default=None,
        help='Variable for the Z axis (generates a 3D scatterplot if provided)'
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

    start_server(args.config_filepath)

    scatterplot(args.x, args.y, args.z)

    if args.kill_server is True:
        end_server()


if __name__ == '__main__':
    main()
