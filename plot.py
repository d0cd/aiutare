#!/usr/bin/env python3

import sys
import argparse
from bin.plotting.test_scatterplot import scatterplot
from bin.plotting.test_3Dgrapher import scatterplot_3d


def main():
    # TODO: parse all args here using argparse

    scatterplot()
    scatterplot_3d()


if __name__ == '__main__':
    main()
