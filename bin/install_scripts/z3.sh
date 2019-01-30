git clone https://github.com/FedericoAureliano/z3.git tools/z3_src

pushd tools/z3_src
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

cp tools/z3_src/build/z3 tools/z3