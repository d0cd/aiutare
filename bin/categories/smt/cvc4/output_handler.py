import sys
import mongoengine
import importlib
from importlib import util

spec = importlib.util.spec_from_file_location("schemas", "bin/categories/smt/schemas.py")
schemas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas)


# Parses the stdout + stderr output from running the problem
# and extracts useful information
def output_handler(nickname, instance, output, elapsed):
    result = 'error'

    if 'UNSAT' in output or 'unsat' in output:
        result = 'unsat'
    elif 'SAT' in output or 'sat' in output:
        result = 'sat'
    elif 'TIMEOUT' in output or 'timeout' in output:
        result = output
    elif 'UNKNOWN' in output or 'unknown' in output:
        result = 'unknown'
    else:
        print(instance, ': Couldn\'t parse output', file=sys.stderr)

    write_results(nickname, instance, result, elapsed)


# Formats and writes information to the database
def write_results(nickname, instance, result, elapsed):

    mongoengine.connect('smt_database')
    stripped_instance = instance.split("/", 2)[2]

    if not schemas.SMTInstance.objects(filename=stripped_instance):
        schemas.SMTInstance.objects(filename=stripped_instance).update_one(upsert=True, set__filename=stripped_instance)

    this_instance = schemas.SMTInstance.objects.get(filename=stripped_instance)

    this_result = schemas.SMTResult(program="cvc4")
    this_result.nickname = nickname
    this_result.instance = this_instance
    this_result.result = result
    this_result.elapsed = elapsed
    this_result.save(force_insert=True)
