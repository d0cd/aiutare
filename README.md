# AIUTARE
Automated Analysis, Regression, and Evaluation

### Setup
- See the [Setup wiki page](https://github.com/FedericoAureliano/aiutare/wiki/Setup) for creating the config and other necessary files
```
./setup.py
```
- (Currently written only for Ubuntu 16.04 and 18.04)

### Usage
```
./aiutare.py [absolute path to config.json file] [number of runs; 1 if omitted]
```

### For Development
- To view all contents of the database:
```
python3 -m bin.test_read_db
```
- To drop the current database:
```
python3 -m bin.drop_databases
```