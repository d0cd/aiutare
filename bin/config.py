config = {'schemas': 'categories.sat.schemas', 'file_extension': 'cnf', 'timeout': 30.0, 'database_name': 'sat_database', 'commands': {'minisat': {'minisat_stock': 'minisat -cpu-lim=33', 'minisat_clone': 'minisat -cpu-lim=33'}, 'syrup': {'syrup_stock': 'categories/sat/tools/syrup/syrup/bin/glucose-syrup -nthreads=8 -maxmemory=50000 -cpu-lim=33'}, 'maple': {'maple_stock': 'categories/sat/tools/maple/MapleLRB_LCMoccRestart/sources/simp/glucose_static -cpu-lim=33'}}, 'handlers': {'minisat': 'categories.sat.minisat_handler', 'syrup': 'categories.sat.syrup_handler', 'maple': 'categories.sat.maple_handler'}, 'instances': 'categories/sat/instances'}
