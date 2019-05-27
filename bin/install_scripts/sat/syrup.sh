#!/usr/bin/env bash

wget -O ../../../tools/sat/syrup "https://baldur.iti.kit.edu/sat-competition-2017/solvers/parallel/syrup.zip"
cd ../../../tools/sat/syrup
make

# TODO: write to correct "solvers" JSON file with command to run