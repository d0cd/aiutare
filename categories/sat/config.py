# All filepaths should be relative
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
    "commands":  # TODO: replace with executable filepaths for your local machine
        {
            "syrup":
                {
                    "syrup_stock": "categories/sat/tools/syrupsat -nthreads=1 -cpu-lim=3300"
                },
            "minisat":
                {
                    "minisat_stock": "categories/sat/tools/minisat -cpu-lim=3300",
                },
            "maple":
                {
                    "maple_stock": "categories/sat/tools/maplesat -cpu-lim=3300"
                }
        }
}
