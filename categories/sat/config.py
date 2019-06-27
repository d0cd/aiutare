config = {
    "file_extension": "cnf",
    "database_name": "sat_database",
    "timeout": 30.0,

    "instances":    "categories/sat/instances",
    "schemas":      "categories/sat/schemas.py",
    "handlers":
        {
            "syrup":    "categories/sat/syrup_handler.py",
            "minisat":  "categories/sat/minisat_handler.py",
            "maple":    "categories/sat/maple_handler.py"
        },
    "commands":
    # These CAN be absolute paths to the tools on your machine (if you'd rather not place them in "categories")
        {
            "syrup":
                {
                    "syrup_stock": "categories/sat/tools/syrup/syrup/bin/glucose-syrup -nthreads=8 -maxmemory=50000 -cpu-lim=33"
                },
            "minisat":
                {
                    "minisat_stock": "minisat -cpu-lim=33",
                    "minisat_clone": "minisat -cpu-lim=33"
                },
            "maple":
                {
                    "maple_stock": "categories/sat/tools/maple/MapleLRB_LCMoccRestart/sources/simp/glucose_static -cpu-lim=33"
                }
        }
}
