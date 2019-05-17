if [ ! -d "instances/random" ]; then
   mkdir instances/random
   fi

for i in {1..10}
do
	for j in {1..10}
	do
		bin/stringfuzz/bin/stringfuzzg -r random-ast -w -m -n $(( ( RANDOM % 5 ) + 1 )) -d $(( ( RANDOM % $i ) + 1 )) -v $(( ( RANDOM % $i ) + 1 )) -t $(( ( RANDOM % $i ) + 1 )) -l $(( ( RANDOM % $i ) + 1 )) -x $(( ( RANDOM % $i ) + 1 )) > instances/random/$i-$j.smt2
	done
done
