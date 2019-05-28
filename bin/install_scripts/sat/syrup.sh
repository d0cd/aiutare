#!/usr/bin/env bash

wget -O tools/sat/syrup_zipped "https://baldur.iti.kit.edu/sat-competition-2017/solvers/parallel/syrup.zip"
cd tools/sat
mkdir syrup
unzip syrup_zipped -d syrup
cd syrup/syrup
make
cd ../..
rm syrup_zipped

# TODO: write to correct "solvers" JSON file with command to run