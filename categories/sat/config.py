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
                    "syrup_stock": "categories/sat/tools/syrupsat -nthreads=8 -maxmemory=50000 -cpu-lim=33"
                },
            "minisat":
                {
                    "minisat_stock": "categories/sat/tools/minisat -cpu-lim=33",
                    "minisat_clone": "categories/sat/tools/minisat -cpu-lim=33"
                },
            "maple":
                {
                    "maple_stock": "categories/sat/tools/maplesat -cpu-lim=33"
                }
        }
}
