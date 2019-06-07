#!/usr/bin/env bash

# Start MongoDB if not already running
if ! pgrep mongod > /dev/null ; then
   mongod --dbpath ./results --logpath ./results/log/mongodb.log &
fi

python3 bin/parse_instances.py $1

num_benches=1
if [[ $# -eq 2 && $2 -gt 1 ]]; then
   num_benches=$2
fi

for ((n=0;n<${num_benches};n++)); do
   python3 bin/bench.py $1
done

python3 bin/analyze.py $1