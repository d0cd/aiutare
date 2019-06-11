# AIUTARE
Automated Analysis, Regression, and Evaluation

### Setup
- See the [Setup wiki page](https://github.com/FedericoAureliano/aiutare/wiki/Setup) for creating the config and other necessary files
```
./prepare.sh [absolute path to config.json file]
```
- (Currently written only for Ubuntu 16.04 and 18.04)

### Usage
```
./run.sh [number of runs; 1 if omitted]
```

### Cleanup
- To kill MongoDB processes and purge logs when finished:
```
./cleanup.sh
```
