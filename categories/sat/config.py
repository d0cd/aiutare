config = {
    "file_extension": "cnf",
    "database_name": "sat_database",
    "timeout": 3000.0,

    "instances":    r"C:\Users\Owner\PycharmProjects\aiutare\categories\sat\minisat_handler.py",
    "schemas":      r"categories/sat/schemas.py",
    "handlers":
        {
            "syrup":    r"categories/sat/syrup_handler.py",
            "minisat":  r"categories/sat/minisat_handler.py",
            "maple":    r"categories/sat/maple_handler.py"
        },
    "commands":
    # These CAN be absolute paths to the tools on your machine (if you'd rather not place them in "categories")
        {
            "syrup":
                {
                    "syrup_stock": r"categories/sat/tools/syrupsat -nthreads=1 -cpu-lim=3300"
                },
            "minisat":
                {
                    "minisat_stock": r"categories/sat/tools/minisat -cpu-lim=3300",
                },
            "maple":
                {
                    "maple_stock": r"categories/sat/tools/maplesat -cpu-lim=3300"
                }
        }
}
