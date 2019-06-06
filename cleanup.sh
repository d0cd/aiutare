#!/usr/bin/env bash

mongo_process=$(pgrep mongod)
sudo kill ${mongo_process}

# TODO: possibly add log file rotating if they grow out of hand