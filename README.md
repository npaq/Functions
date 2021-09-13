# Functions

Package of helper functions used in the radiological consequences calculation script: https://github.com/npaq/radiological-impact-aircraft-crash

# Installation

This module was converted to a package to make it easier to install for other contributors to the project, not relying on local paths anymore.
This package can be installed using either of the following commands if you use SSH

    pip install -e git+ssh://git@github.com/npaq/Functions.git@main#egg=rdo_functions
    pipenv install -e git+ssh://git@github.com/npaq/Functions.git@main#egg=rdo_functions

One of the following commands if you don't use SSH

	pip install -e git+ssh://git@github.com/npaq/Functions.git@main#egg=rdo_functions
	pipenv install -e git+ssh://git@github.com/npaq/Functions.git@main#egg=rdo_functions

__NOTE:__ if you are not using SSH keys as authentication method for github, you need to change git+ssh to git+https in the above commands. Doing so you will be asked for a password. Github does not support passwords anymore, you must create an authentication token through the github website: click on your user icon > settings > Developper Settings > Personal access tokes > generate new token. Give this token a name, expiration date, select the scope (you only need all the _repo_ boxes) then generate token. Keep it safe, just like a password, but keep a copy of it as github will never show this to you anymore.

# Usage

```python
import rdo_functions

rdo_functions.function_name()
```

# List of available functions

- from __calculations.py__:
    - radiologicalImpact
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

# Updating to latest version

Run either of the following commands

    pip update rdo_functions
    pipenv update rdo_functions

# Uninstall

To uninstall the package run either of the following commands depending on the one you used for installation.

    pip uninstall rdo_functions
    pipenv uninstall rdo_functions
