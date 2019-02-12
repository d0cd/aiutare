#!/bin/bash

if [ ! -d "tools" ]; then
   mkdir tools
   bin/install_scripts/cvc4.sh
   bin/install_scripts/z3.sh
fi

if [ ! -d "images" ]; then
   mkdir images
fi

if [ ! -d "results" ]; then
   mkdir results
fi

if [ ! -d "instances" ]; then
   mkdir instances
fi

for lib_call_depth in {5..40..5}
do
   for iteration in {1..10}
   do
      stringfuzzg -r clever --client-depth 50 --clever-depth $lib_call_depth > instances/clever-$client_depth-$lib_call_depth-$iteration.smt2
   done
done