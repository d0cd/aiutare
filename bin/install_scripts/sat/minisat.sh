#!/usr/bin/env bash

cd tools/sat
git clone https://github.com/niklasso/minisat.git
cd minisat
make config prefix=../../../tools/sat
make install