#!/usr/bin/env python3

import subprocess
import setuptools

# TODO: other python code for installation goes here (call different script for each OS?)

subprocess.call(['./bin/install_mongodb.sh'])

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiutare-finnbarroc",
    version="0.0.1",
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
        "Operating System :: Ubuntu 16.04 and 18.04",
    ],
    install_requires=['mongoengine', 'matplotlib', 'numpy']
)
