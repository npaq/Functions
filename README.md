# Functions

Package of helper functions used in the radiological consequences calculation script: https://github.com/npaq/radiological-impact-aircraft-crash

# Installation

This module was converted to a package to make it easier to install for other contributors to the project, not relying on local paths anymore.
This package can be installed using either of the following commands

    pip install git+ssh://git@github.com:npaq/Functions.git 
    pipenv install git+ssh://git@github.com:npaq/Functions.git

# Usage

```python
import Functions

Functions.function_name()
```

# List of available functions

- from __Calculations.py__:
    - radiologicalImpact
- from __Data_handling.py__:
    - db_list_of_tables
    - db_fetch_data
    - db_create_dictionary
    - file_create_dictionary
    - create_db
    - create_table
    - outputTablesRadiologicalImpact_pivoted
    - insert_table
    - write_csv
- from __Utilities.py__:
    - get_list_of_files

