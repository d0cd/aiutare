#!/usr/bin/env bash

wget -O tools/sat/maple_zipped "https://baldur.iti.kit.edu/sat-competition-2017/solvers/main/MapleLRB_LCMoccRestart.zip"
cd tools/sat
mkdir maple
unzip maple_zipped -d maple
cd maple/MapleLRB_LCMoccRestart/sources/simp
make rs
cd ../../../..
rm maple_zipped