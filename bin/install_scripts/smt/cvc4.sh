#!/usr/bin/env bash
wget -O tools/smt/cvc4 "http://cvc4.cs.stanford.edu/downloads/builds/x86_64-linux-opt/cvc4-1.6-x86_64-linux-opt"
chmod 755 tools/smt/cvc4

# TODO: write to correct "solvers" JSON file with command to run