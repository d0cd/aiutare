#!/usr/bin/env python3
import os
import setuptools
import platform
from subprocess import run


print("Creating directory structure")
os.makedirs("results/log", exist_ok=True)
os.makedirs("images", exist_ok=True)

uid = os.getuid()
os.chown("results", uid, -1)
os.chown("results/log", uid, -1)
os.chown("images", uid, -1)

print("Calling correct OS MongoDB install script")
operating_system = platform.system()
if operating_system == "Linux":
    run(['./bin/install_mongodb/linux.sh'])
else:
    print("OS not currently supported :(")
    exit(1)

path = "results"
for root, dirs, files in os.walk(path):
    for file in dirs:
        os.chmod(os.path.join(root, file), 0o0777)
    for file in files:
        os.chmod(os.path.join(root, file), 0o0777)


print("Calling setuptools.setup function")
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiutare",
    version="1.0",
    author="Federico Mora, Lukas Finnbarr O'Callahan",
    author_email="fmora@cs.toronto.edu, lukasocallahan@gmail.com",
    description="A benchmarking framework for SAT, SMT, and equivalence checking programs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FedericoAureliano/aiutare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        'mongoengine',
        'matplotlib',
        'numpy',
        'progressbar2',
        'pymongo',
        'psutil',
        'scipy'
    ]
)
