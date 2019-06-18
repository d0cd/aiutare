#!/usr/bin/env bash

# Start MongoDB if not already running
if ! pgrep mongod > /dev/null ; then
   mongod --dbpath ./results --logpath ./results/log/mongodb.log &
fi

python3 ./parse_instances.py

num_benches=1
if [[ $# -eq 1 && $1 -gt 1 ]]; then
   num_benches=$1
fi

for ((n=0;n<${num_benches};n++)); do
   python3 ./bench.py
done

python3 ./analyze.py