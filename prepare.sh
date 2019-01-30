#!/bin/bash

mkdir images
mkdir results
mkdir instances
cd instances
mkdir random
for i in {5..10}
do
   for j in {1..10}
   do
      stringfuzzg -r random-ast -w -m -n $(( ( RANDOM % 5 ) + 1 )) -d $(( ( RANDOM % $i ) + 1 )) -v $(( ( RANDOM % $i ) + 1 )) -t $(( ( RANDOM % $i ) + 1 )) -l $(( ( RANDOM % $i ) + 1 )) -x $(( ( RANDOM % $i ) + 1 )) > random/$i-$j.smt2
   done
done

wget -O bin/cvc4 "http://cvc4.cs.stanford.edu/downloads/builds/x86_64-linux-opt/cvc4-1.6-x86_64-linux-opt"
chmod 755 bin/cvc4