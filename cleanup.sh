#!/usr/bin/env bash

mongo_process=$(pgrep mongod)
kill ${mongo_process}

rm results/log/mongodb.log