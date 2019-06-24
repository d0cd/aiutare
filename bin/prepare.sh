#!/bin/bash

mkdir -p results/log
mkdir images

user="$(id -u -n)"
sudo chown -R ${user} ./results
sudo chown -R ${user} ./images

