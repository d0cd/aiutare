import json
import mongoengine
import importlib
from importlib import util

CONFIG = json.loads(open("bin/config.json", 'r').read())
spec = importlib.util.spec_from_file_location("schemas", CONFIG["schemas"])
schemas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas)


def main():
    mongoengine.connect(CONFIG["database_name"])

    print("%d Instances found" % len(schemas.Instance.objects()))
    print("%d Results found" % len(schemas.Result.objects()))

    for Instance in schemas.Instance.objects():
        print(Instance.to_json())

    for Result in schemas.Result.objects():
        print(Result.to_json())


if __name__ == '__main__':
    main()
