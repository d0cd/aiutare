#!/usr/bin/env bash

if [[ ! -d "instances/smt/random" ]]; then
   mkdir instances/smt/random
   fi

for i in 1 2 3 4 5 6 7 8 9 10
do
	for j in 1 2 3 4 5 6 7 8 9 10
	do
		bin/stringfuzz/bin/stringfuzzg -r random-ast -w -m -n $(( ( RANDOM % 5 ) + 1 )) -d $(( ( RANDOM % $i ) + 1 )) -v $(( ( RANDOM % $i ) + 1 )) -t $(( ( RANDOM % $i ) + 1 )) -l $(( ( RANDOM % $i ) + 1 )) -x $(( ( RANDOM % $i ) + 1 )) > instances/smt/random/${i}-${j}.smt2
	done
done
