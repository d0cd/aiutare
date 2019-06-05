import mongoengine
import importlib
from importlib import util

spec = importlib.util.spec_from_file_location("schemas", "bin/categories/sat/schemas.py")
schemas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas)


def main():
    mongoengine.connect('sat_database')

    print("%d SATInstances found" % len(schemas.SATInstance.objects()))
    print("%d SATResults found" % len(schemas.SATResult.objects()))

    for SATInstance in schemas.SATInstance.objects():
        print(SATInstance.to_json())

    for SATResult in schemas.SATResult.objects():
        print(SATResult.to_json())


if __name__ == '__main__':
    main()
