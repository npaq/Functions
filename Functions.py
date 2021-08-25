import os 
import sqlite3
#---------------------------------------------------------------------------------
#                                   FUNCTIONS
#---------------------------------------------------------------------------------

# List of tables in a DB
def db_listOfTables(conn):
    """
    conn : connection to the DB
    tables : retun the list of table names in the DB
    """
    # Connection to the DB
    cursor = conn.cursor()
    
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [Tuple[0] for Tuple in tables]
    # Remove tables where 'meta_' is in the name of the table (i.e. metadata not used in the program)
    tables = [x for x in tables if 'meta_' not in x]
    return tables

# Fetching data in a DB table
def db_fetchingData(table, conn):
    """
    table [string] : table name in the DB
    conn : connection to the DB to which the table belongs
    """
    selectQuery = 'SELECT * FROM ' + table
    cursor = conn.cursor()
    res = cursor.execute(selectQuery)
    columns = [Tuple[0] for Tuple in res.description]
    columns = [x for x in columns if 'Meta_' not in x]
    
    selectQuery = 'SELECT '
    for column in columns:
        if column != columns[-1]:
            selectQuery = selectQuery + column + ', '
        else:
            selectQuery = selectQuery + column + ' '
    selectQuery = selectQuery + 'FROM ' + table
    cursor.execute(selectQuery)
    rows = cursor.fetchall()

    columns = columns[1:] 
    list = [rows, columns]
    return(list)

# Creating a dictionary from a DB
def db_creatingDictionary(items, keys, key2):
    """
    items [list] : rows extracted from a table. Each row is a tuple corresponding to a row in the table
    keys [list] : keys of the dictionary to be created by the function (optional)
    key [constant, string] : second key of the dictionary to be created by the function (optional)
    """
    dic = {}
    if keys and not key2:
        for item in items:
            index = 1
            for key in keys:
                dic[item[0], key] = item[index]
                if index < len(keys) :
                    index = index + 1
    elif keys and key2:
        for item in items:
            index = 1
            for key in keys:
                dic[item[0], key, key2] = item[index]
                if index < len(keys) :
                    index = index + 1
    elif not keys and key2:
        dic[key2] = items
    else: 
        for item in items:
            dic[item[0]] = item[1]
    return dic

# Creating a dictionary from raw data in a file (txt)
def file_creatingDictionary(data):
    """
    data [list] : rows in the file 
    split() : create a list by splitting the line around "="
    strip() : remove white space
    replace() : replace ',' by '.' in order to be converted into a float with the method float()
    float() : convert the string into a float
    """
    dic = {r.split('=')[0].strip(): float(r.split('=')[1].strip().replace(',', '.')) for r in data}
    return dic

# Create output DB
def createOutputDB(path):
    """
    Create the DB with the results
    Default name of the DB: Results.db
    Return the connection the DB 
    """
    # output DB connection
    # Default name of the output DB
    defaultDdName = "Results.db"

    outputDdName = input("Name of the output DB (default : Results.db): ")
    if outputDdName =='': 
        outputDdName = defaultDdName
    else:
        outputDdName = outputDdName.replace(' ', '_')
        outputDdName = outputDdName + '.db'
    
    if os.sys.platform == 'win32':
        path_output = path + '\\' + outputDdName
    else: 
        path_output = path + '/' + outputDdName
    
    conn = sqlite3.connect(path_output)
    return conn


# Create output tables for radiological consequences
def outputTablesRadiologicalImpact(conn, tableName, colNames):
    cursor = conn.cursor()
    # Drop table Result
    cursor.execute( 
        """
        DROP TABLE IF EXISTS {tab};
        """.format(tab = tableName)
        )
    # Create table results (i.e. tableName)
    query = """CREATE TABLE IF NOT EXISTS {tab}(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE
                , """.format(tab = tableName)
    for c in colNames:
        if c != colNames[-1]: 
            query = query + c + ' TEXT, '
        else:
            query = query + 'Dose REAL);'
    cursor.execute(query) 
    conn.commit()

# Create output tables (pivoted) for radiological consequences
def outputTablesRadiologicalImpact_pivoted(conn, tableName, note_lst, doseTypes, ageGroups):
    """
    Create 2 tables in the output DB. 
        - Comment added by the user : Note
        - Results of the calculation by unit, scenario, isotope, dose type and age group. 
        The name of the table is given by tableName
    List of parameters : 
        - conn : connection to the output DB 
        - tableName [string] : name of the result table
        - note_lst [list] : list where each row contains a line of comment. 
        The function asks to add a new line of comment (optional)
        - doseTypes [list] : list of dose types to be considered 
        - ageGroup [list] : list of age group to be considered
    """
    cursor = conn.cursor()
    note = input("Insert a note (optional): ")
    if note : note_lst.append(note)
    # Drop table Result
    cursor.execute( 
        """
        DROP TABLE IF EXISTS {tab};
        """.format(tab = tableName)
        )
    # Drop table Note
    cursor.execute( 
        """
        DROP TABLE IF EXISTS Note;
        """
    )
    # Create table Note
    cursor.execute( \
        """
        CREATE TABLE IF NOT EXISTS Note(
            Note TEXT
            );"""
    ) 
    # Insert each line of comment into Table Note
    for n in note_lst:
        cursor.execute(\
            """
            INSERT INTO Note VALUES (?);    
            """, (n, )
        )
    # Create table results (i.e. tableName)
    query = """CREATE TABLE IF NOT EXISTS {tab}(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE
                , Unit TEXT
                , Scenario TEXT
                , Isotope TEXT
                ,  """.format(tab = tableName)
    for doseType in doseTypes:
        for ageGroup in ageGroups:
            if doseType == doseTypes[-1] and ageGroup == ageGroups[-1]:
                query = query + doseType + '_' + ageGroup + ' ' + 'REAL );'
            else:
                query = query + doseType + '_' + ageGroup + ' ' + 'REAL ' + ', '
    cursor.execute(query) 
    conn.commit()