#!/usr/bin/env bash

# Start MongoDB if not already running
if ! pgrep mongod > /dev/null ; then
   sudo mongod --dbpath ./results --logpath ./results/log/mongodb.log --logappend &
fi

python3 bin/bench.py $1
# python3 bin/test_read_db.py
python3 bin/analyze.py $1