#!/usr/bin/env bash

# Kill MongoDB if running
if pgrep mongod > /dev/null ; then
   mongo_process=$(pgrep mongod)
   kill ${mongo_process}
fi

rm results/log/mongodb.log
rm bin/written_instances.json