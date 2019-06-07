import sys
import glob
import json
import importlib
from importlib import util


def main():
    category_name = sys.argv[1]
    instances = glob.glob("instances/%s/**/*.*" % category_name, recursive=True)
    print("%d %s instance(s) found" % (len(instances), category_name))

    spec = importlib.util.spec_from_file_location("schemas", "bin/categories/%s/schemas.py" % category_name)
    schemas = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schemas)

    schemas.write_instances(instances)

    with open("bin/written_instances.json", 'w') as written_instances:
        written_instances.write(json.dumps(instances))


if __name__ == '__main__':
    main()
