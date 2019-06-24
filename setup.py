#!/usr/bin/env python3

from subprocess import run, Popen, DEVNULL
import setuptools
import platform
import time

# TODO: create directory structure



# TODO: other python code for installation goes here (call different script for each OS?)
# operating_system = platform.system()
# if operating_system == "Linux":
#     run(['./bin/install_mongodb/linux.sh'])

Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
      " --replSet monitoring_replSet".split(), stdout=DEVNULL)



time.sleep(5)


Popen("mongo --eval 'rs.initiate()' &".split())
exit(0)







# with open("README.md", "r") as fh:
#     long_description = fh.read()
#
# setuptools.setup(
#     name="aiutare-finnbarroc",
#     version="0.0.1",
#     author="Federico Mora, Lukas Finnbarr O'Callahan",
#     author_email="fmora@cs.toronto.edu, lukasocallahan@gmail.com",
#     description="A benchmarking framework for SAT, SMT, and equivalence checking programs.",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/FedericoAureliano/aiutare",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: Ubuntu 16.04 and 18.04",
#     ],
#     install_requires=['mongoengine', 'matplotlib', 'numpy', 'progressbar2', 'pymongo', 'psutil']
# )
