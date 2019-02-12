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

for client_depth in {5..20..5}
do
   lib_depth=$(expr 25 - $client_depth)
   for (( lib_call_depth = 3; lib_call_depth < $client_depth; lib_call_depth = lib_call_depth + 3 ))
   do 
      for iteration in {1..5}
      do
         stringfuzzg -r clever --client-depth $client_depth --lib-depth $lib_depth --clever-depth $lib_call_depth > instances/clever-$client_depth-$lib_call_depth-$iteration.smt2
      done
   done
done