#!/usr/bin/env bash

# Kill MongoDB if running
if pgrep mongod > /dev/null ; then
   mongo_process=$(pgrep mongod)
   kill ${mongo_process}
fi

rm -f results/log/mongodb.log*
rm -f bin/written_instances.json
