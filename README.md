# Functions

Package of helper functions used in the radiological consequences calculation script: https://github.com/npaq/radiological-impact-aircraft-crash

# Installation

If you want to use this package in another project you can just clone its repository while in your project folder:

    git clone https://github.com/npaq/rdofunctions rdofunctions

If your project is already a git repository, you need to install it as a git submodule. To do so:

	git submodule add https://github.com/npaq/rdofunctions rdofunctions
	git submodule init
	git submodule update

# Usage

```python
import rdofunctions

rdofunctions.function_name()
```

# List of available functions

- from __data_handling.py__:
    - db_list_of_tables
    - db_fetch_data
    - db_create_dictionary
    - file_create_dictionary
    - create_db
    - create_table
    - outputTablesRadiologicalImpact_pivoted
    - insert_table
    - write_csv
- from __utilities.py__:
    - get_list_of_files
