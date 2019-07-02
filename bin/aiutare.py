#!/usr/bin/env python3

import sys

from benching.run import run


def main():
    # TODO: parse all args here using argparse
    config_filepath = sys.argv[1]
    num_bench = 1
    if len(sys.argv) > 2:
        num_bench = int(sys.argv[2])

    run(config_filepath, num_bench)


if __name__ == '__main__':
    main()
