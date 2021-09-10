# Functions

Package of helper functions used in the radiological consequences calculation script: https://github.com/npaq/radiological-impact-aircraft-crash

# Installation

This module was converted to a package to make it easier to install for other contributors to the project, not relying on local paths anymore.
This package can be installed using either of the following commands

    pip install -e git+ssh://git@github.com/npaq/Functions.git@main#egg=functions 
    pipenv install -e git+ssh://git@github.com/npaq/Functions.git@main#egg=functions

__NOTE:__ if you are not using SSH keys as authentication method for github, you need to change git+ssh to git+https in the above commands. Doing so you will be asked for a password. Github does not support passwords anymore, you must create an authentication token through the github website: click on your user icon > settings > Developper Settings > Personal access tokes > generate new token. Give this token a name, expiration date, select the scope (you only need all the _repo_ boxes) then generate token. Keep it safe, just like a password, but keep a copy of it as github will never show this to you anymore.

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

