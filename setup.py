#!/usr/bin/env python3
import os
import sys
import platform
from subprocess import run, call


PIP_DEPENDENCIES = [
        'pymongo',
        'mongoengine',
        'progressbar2',
        'tabulate',
        'numpy',
        'scipy',
        'plotly'
]


def pip_install(package):
    call([sys.executable, "-m", "pip", "install", package])


def main():
    print("Creating directory structure")
    os.makedirs("results/log", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    os.makedirs("bin/verification/v_results/log", exist_ok=True)

    uid = os.getuid()
    os.chown("results", uid, -1)
    os.chown("results/log", uid, -1)
    os.chown("plots", uid, -1)

    os.chown("bin/verification/v_instances", uid, -1)

    print("Calling correct OS MongoDB install script")
    operating_system = platform.system()
    if operating_system == "Linux":
        run(['./bin/install_mongodb/linux.sh'])
    else:
        print("OS not currently supported :(")
        exit(1)

    for root, dirs, files in os.walk("results"):
        for file in dirs:
            os.chmod(os.path.join(root, file), 0o0777)
        for file in files:
            os.chmod(os.path.join(root, file), 0o0777)

    for dependency in PIP_DEPENDENCIES:
        pip_install(dependency)


if __name__ == '__main__':
    main()
