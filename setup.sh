#!/bin/bash

# GENERAL:
# Needed for either SAT or SMT

# "instances" contains benchmarks and other problem cases
if [[ ! -d "instances" ]]; then
   mkdir instances
fi

# "tools" contains the solvers to run
if [[ ! -d "tools" ]]; then
   mkdir tools
fi

# "results" contains the output of bench.py in .csv format
if [[ ! -d "results" ]]; then
   mkdir results
fi

# "images" contains graphs generated from the data in "results"
if [[ ! -d "images" ]]; then
   mkdir images
fi

sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install matplotlib
pip3 install numpy


# SAT ONLY:
# Enabled by default, or specified with parameter "-sat"
if [[ $# -eq 0 || $1 = "-sat" ]]; then

   if [[ ! -d "instances/sat" ]]; then
      mkdir instances/sat
   fi

   if [[ ! -d "tools/sat" ]]; then
      mkdir tools/sat
   fi

   if [[ ! -d "results/sat" ]]; then
      mkdir results/sat
   fi

   if [[ ! -d "images/sat" ]]; then
      mkdir images/sat
   fi

   # comment out any unneeded tools below:
   bin/install_scripts/sat/minisat.sh
   bin/install_scripts/sat/syrup.sh

fi


# SMT ONLY:
# Enabled by default, or specified with parameter "-smt"
if [[ $# -eq 0 || $1 = "-smt" ]]; then

   if [[ ! -d "instances/smt" ]]; then
      mkdir instances/smt
   fi

   if [[ ! -d "tools/smt" ]]; then
      mkdir tools/smt
   fi

   if [[ ! -d "results/smt" ]]; then
      mkdir results/smt
   fi

   if [[ ! -d "images/smt" ]]; then
      mkdir images/smt
   fi

   # comment out any unneeded tools below:
   bin/install_scripts/smt/cvc4.sh
   bin/install_scripts/smt/z3.sh

   git clone https://github.com/dblotsky/stringfuzz.git bin/stringfuzz
   pushd bin/stringfuzz
   git checkout random_word_eq
   git pull origin random_word_eq
   python3 setup.py install --user
   popd

   if [[ ! -d "instances/smt/random" ]]; then
      mkdir instances/smt/random
   fi

   for i in {5..10}
   do
      for j in {1..10}
      do
         bin/stringfuzz/bin/stringfuzzg -r random-ast -w -m -n $(( ( RANDOM % 5 ) + 1 )) -d $(( ( RANDOM % $i ) + 1 )) -v $(( ( RANDOM % $i ) + 1 )) -t $(( ( RANDOM % $i ) + 1 )) -l $(( ( RANDOM % $i ) + 1 )) -x $(( ( RANDOM % $i ) + 1 )) > instances/smt/random/$i-$j.smt2
      done
   done
fi