import mongoengine
import importlib
from subprocess import Popen
import psutil
from bin.config import config
schemas = importlib.import_module(config["schemas"])


def main():
    Popen("mongod --dbpath ./results --logpath ./results/log/mongodb.log".split() +
          " --replSet monitoring_replSet".split())

    mongoengine.connect(config["database_name"], replicaset="monitoring_replSet")
    print("%d Instances found" % len(schemas.Instance.objects()))
    print("%d Results found" % len(schemas.Result.objects()))

    for Instance in schemas.Instance.objects():
        print(Instance.to_json())

    for Result in schemas.Result.objects():
        print(Result.to_json())

    mongoengine.connection.disconnect()

    procname = "mongod"

    for proc in psutil.process_iter():
        if proc.name() == procname:
            proc.kill()


if __name__ == '__main__':
    main()
