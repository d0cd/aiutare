import mongoengine
import importlib
from importlib import util

spec = importlib.util.spec_from_file_location("schemas", "bin/categories/smt/schemas.py")
schemas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemas)


def main():
    mongoengine.connect('smt_database')

    print("%d SMTInstances found" % len(schemas.SMTInstance.objects()))
    print("%d SMTResults found" % len(schemas.SMTResult.objects()))

    for SMTInstance in schemas.SMTInstance.objects():
        print(SMTInstance.to_json())

    for SMTResult in schemas.SMTResult.objects():
        print(SMTResult.to_json())


if __name__ == '__main__':
    main()
