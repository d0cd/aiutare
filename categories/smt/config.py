config = {
    "file_extension": "smt2",
    "database_name": "smt_database",
    "timeout": 30.0,

    "instances":    "categories/smt/instances",
    "schemas":      "categories/smt/schemas.py",
    "handlers":
        {
            "z3":    "categories/smt/z3_handler.py",
            "cvc4":  "categories/smt/cvc4_handler.py"
        },
    "commands":
    # These CAN be absolute paths to the tools on your machine (if you'd rather not place them in "categories")
        {
            "z3":
                {
                    "z3_master": "categories/smt/tools/z3_master smt.string_solver=z3str3 -T:33",
                    "z3_federico": "categories/smt/tools/z3_federico smt.string_solver=z3str3 -T:33",
                },
            "cvc4":
                {
                    "cvc4_models": "categories/smt/tools/cvc4 --lang smt --strings-exp --tlimit=33000 -q --produce-models",
                    "cvc4_no_models": "categories/smt/tools/cvc4 --lang smt --strings-exp --tlimit=33000 -q",
                }
        }
}
