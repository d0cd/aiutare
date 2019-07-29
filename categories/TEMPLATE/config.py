# All filepaths should be relative TODO: fill in with necessary information using the indicated formats
config = {
    "file_extension": "TODO",  # Omit the period "." from the file extension of your benchmarks
    "database_name": "TODO_database",
    "timeout": 30.0,

    "instances":    "your/instances/directory",  # Directory containing your benchmarks
    "schemas":      "your/schemas/file.py",
    "handlers":
        {
            "program1": "path/to/program1_handler.py",
            "program2": "path/to/program2_handler.py",
        },
    "commands":
        {
            "program1":
                {
                    "program1_stock": "path/to/program1/executable -params -added -here"
                },
            "program2":
                {
                    "program2_stock": "path/to/program2/executable -params -added -here"
                },
        }
}
