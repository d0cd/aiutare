

config = {
    "database_name": "sat_database",
    "timeout": 30.0,

    "absolute_filepaths":   False,
    "instances":    "bin/sat/instances",
    "schemas":      "bin/sat/schemas.py",
    "handlers":
        {
            "syrup": "bin/sat/syrup_handler.py",
            "minisat": "bin/sat/minisat_handler.py",
            "maple": "bin/sat/maple_handler.py"
        },
    "commands":
        {
            "syrup":
                {
                    "syrup_stock": "tools/sat/syrup/syrup/bin/glucose-syrup -nthreads=8 -maxmemory=50000 -cpu-lim=33"
                },
            "minisat":
                {
                    "minisat_stock": "minisat -cpu-lim=33",
                    "minisat_clone": "minisat -cpu-lim=33"
                },
            "maple":
                {
                    "maple_stock": "tools/sat/maple/MapleLRB_LCMoccRestart/sources/simp/glucose_static -cpu-lim=33"
                }
        }
}
