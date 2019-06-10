import sys
import mongoengine
import importlib
from importlib import util

spec = importlib.util.spec_from_file_location("schemas", "file/path/schemas.py")  # TODO: absolute schema file path here
schemas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas)


# Parses the stdout + stderr output from running the problem
# and extracts useful information
def output_handler(nickname, instance, output, elapsed):
    result = 'error'

    # TODO: Fill in the statements below to extract needed information from program output
    # if 'unsat' in output:
    #     result = 'unsat'
    # elif 'sat' in output:
    #     result = 'sat'
    # elif 'timeout' in output:
    #     result = output
    # elif 'unknown' in output:
    #     result = 'unknown'
    #
    # else:
    #     print(instance, ': Couldn\'t parse output', file=sys.stderr)

    write_results(nickname, instance, result, elapsed)


# Formats and writes information to the database
def write_results(nickname, instance, result, elapsed):

    mongoengine.connect("database_name")  # TODO: replace with name of your database here

    this_instance = schemas.Instance.objects.get(filename=instance.split("/", 1)[1])

    this_result = schemas.Result(program="program_directory_name")  # TODO: replace with program directory name here
    this_result.nickname = nickname
    this_result.instance = this_instance
    this_result.result = result
    this_result.elapsed = elapsed
    # TODO: write other data as specified by your schema here before saving
    this_result.save(force_insert=True)
