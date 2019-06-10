import glob
import json
import importlib
from importlib import util


def main():
    config_file = open("bin/config.json", 'r').read()
    config = json.loads(config_file)

    instances = glob.glob("%s/**/*.*" % config["instances"], recursive=True)
    print("%d instance(s) found" % len(instances))

    spec = importlib.util.spec_from_file_location("schemas", config["schemas"])
    schemas = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schemas)

    schemas.write_instances(instances)

    with open("bin/written_instances.json", 'w') as written_instances:
        written_instances.write(json.dumps(instances))


if __name__ == '__main__':
    main()
