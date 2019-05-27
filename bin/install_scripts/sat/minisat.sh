#!/usr/bin/env bash

git clone https://github.com/niklasso/minisat.git
cd minisat

make config prefix=../../../tools/sat
make install

# TODO: write to correct "solvers" JSON file with command to run