# AIUTARE
Automated Analysis, Regression, and Evaluation

### Setup
- To create the necessary file structure and install 
specified programs in the "bin/categories" directory (default is all):
```
./prepare.sh [category, e.g. sat]
```
- (Currently written only for Ubuntu 16.04 and 18.04)

### Usage
```
./run.sh [category, e.g. sat] [number of runs; 1 if omitted]
```

### Cleanup
- To kill MongoDB processes when finished:
```
./cleanup.sh
```