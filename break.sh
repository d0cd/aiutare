limit=10

while stringfuzzg -r random-ast -m \
| tee instance.smt25 | timeout $limit z3 -in -T:$limit; do
sleep 0
done