#!/usr/bin/env python3
import os
import sys
import platform
import argparse
from subprocess import call


PIP_DEPENDENCIES = [
        'pymongo',
        'mongoengine',
        'progressbar2',
        'tabulate',
        'numpy',
        'scipy',
        'plotly',
        'psutil'
]


def parse_arguments():
    # create arg parser
    global_parser = argparse.ArgumentParser(description='modular benchmarking framework')

    # global args
    global_parser.add_argument(
        metavar='cfg',
        dest='config_filepath',
        type=str,
        help='absolute filepath to the user-provided config file'
    )

    return global_parser.parse_args()


def pip_install(package):
    call([sys.executable, "-m", "pip", "install", package])


def main():
    args = parse_arguments()

    print("Creating directory structure")
    os.makedirs("results/log", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    if platform.system() != "Windows":
        uid = os.getuid()
        os.chown("results", uid, -1)
        os.chown("results/log", uid, -1)
        os.chown("plots", uid, -1)

    for root, dirs, files in os.walk("results"):
        for file in dirs:
            os.chmod(os.path.join(root, file), 0o0777)
        for file in files:
            os.chmod(os.path.join(root, file), 0o0777)

    for dependency in PIP_DEPENDENCIES:
        pip_install(dependency)

    from bin.mongod_manager import start_server, write_config
    write_config(args.config_filepath)

    try:
        start_server()
    except Exception as e:
        print(e)
        print("Please ensure you have the latest version of MongoDB installed.")


if __name__ == '__main__':
    main()