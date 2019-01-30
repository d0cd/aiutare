#!/bin/bash

if [ ! -d "tools" ]; then
   mkdir tools
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

git clone https://github.com/dblotsky/stringfuzz.git bin/stringfuzz
pushd bin/stringfuzz
git checkout random_word_eq
git pull origin random_word_eq
python3 setup.py install --user
popd

if [ ! -d "instances/random" ]; then
   mkdir instances/random
fi

for i in {5..10}
do
   for j in {1..10}
   do
      bin/stringfuzz/bin/stringfuzzg -r random-ast -w -m -n $(( ( RANDOM % 5 ) + 1 )) -d $(( ( RANDOM % $i ) + 1 )) -v $(( ( RANDOM % $i ) + 1 )) -t $(( ( RANDOM % $i ) + 1 )) -l $(( ( RANDOM % $i ) + 1 )) -x $(( ( RANDOM % $i ) + 1 )) > instances/random/$i-$j.smt2
   done
done

bin/install_scripts/cvc4.sh
bin/install_scripts/z3.sh

pip3 install matplotlib
pip3 install numpy
