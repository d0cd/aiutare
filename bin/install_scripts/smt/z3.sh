#!/usr/bin/env bash
git clone https://github.com/FedericoAureliano/z3.git tools/smt/z3_src

pushd tools/smt/z3_src
git checkout wordeq
git pull origin wordeq

if [ -d "build" ]; then
    rm -rf build
fi

python3 scripts/mk_make.py

pushd build
make
popd
popd

cp tools/smt/z3_src/build/z3 tools/smt/z3