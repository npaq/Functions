import os 
import sqlite3
import csv
#---------------------------------------------------------------------------------
#                                   FUNCTIONS
#---------------------------------------------------------------------------------

# List of tables in a DB
def db_list_of_tables(conn):
    """
    conn : connection to the DB
    Returns the list of table names in the DB
    """
    # Connection to the DB
    cursor = conn.cursor()
    
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [Tuple[0] for Tuple in tables]
    # Remove tables where '_' is the first character of the table (i.e. metadata not used in the program)
    tables = [t for t in tables if t[0] != '_']
    return tables

# Fetching data in a DB table
def db_fetch_data(table, conn):
    """
    table [string] : table name in the DB
    conn : connection to the DB to which the table belongs
    """
    selectQuery = 'SELECT * FROM ' + table
    cursor = conn.cursor()
    res = cursor.execute(selectQuery)
    columns = [Tuple[0] for Tuple in res.description]
    columns = [c for c in columns if c[0] != '_']
    
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
def db_create_dictionary(items, keys, key2):
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
def file_create_dictionary(data):
    """
    data [list] : rows in the file 
    split() : create a list by splitting the line around "="
    strip() : remove white space
    replace() : replace ',' by '.' in order to be converted into a float with the method float()
    float() : convert the string into a float
    """
    dic = {r.split('=')[0].strip(): float(r.split('=')[1].strip().replace(',', '.')) for r in data}
    return dic

# Create DB
def create_db(path, dbName, note):
    """
    Create a sqlite DB
    Default name of the DB: Results.db
    path [str] : location of the DB 
    dbName [str] : name of the db (optional) 
    note_lst : list where each row contains a line of comment. 
    Return the connection the DB 
    """
    if not dbName: 
        # Default name of the output DB
        defaultDdName = "Results"
        dbName = input("Name of the DB (default : Results.db): ")
        if dbName =='': 
            dbName = defaultDdName
    
    dbName = dbName.replace(' ', '_')
    dbName = dbName + '.db'   
    
    if not note: note = []
    n = input("Insert a note (optional): ")
    if n : note.append(n)
    
    # Drop DB before creating it  
    try: 
        os.remove(os.path.join(path, dbName))
        print('The DB ', dbName, ' has been dropped')
        conn = sqlite3.connect(os.path.join(path, dbName))
        print('The DB ', dbName, ' has been created in ', path)
    except:
        print('The DB ', dbName, ' does not exist yet')
        conn = sqlite3.connect(os.path.join(path, dbName))
        print('The DB ', dbName, ' has been created in ', path)
    
    if note : 
        # Drop table Note
        cursor = conn.cursor()
        cursor.execute( 
            """
            DROP TABLE IF EXISTS _Note;
            """
        )
        # Create table Note
        try: 
            cursor.execute( \
                """
                CREATE TABLE IF NOT EXISTS _Note(
                    Note TEXT
                    );"""
            ) 
            # Insert each line of comment into Table Note
            for r in note:
                cursor.execute(\
                    """
                    INSERT INTO _Note VALUES (?);    
                    """, (r, )
                )
            conn.commit()
            print('Table _Note has been created')
        except Exception as ex:
            print(ex)
    return conn


# Create output tables 
def create_table(conn, tableName, colNames):
    tableName = tableName.replace(' ', '_')
    cursor = conn.cursor()
    # Drop table Result
    cursor.execute( 
        """
        DROP TABLE IF EXISTS {tab};
        """.format(tab = tableName)
        )
    # Create table results (i.e. tableName)
    query = """CREATE TABLE IF NOT EXISTS {tab}(
                _id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE
                , """.format(tab = tableName)
    for c in colNames:
        if c != colNames[-1]: 
            query = query + c + ' TEXT, '
        else:
            query = query + c + ' TEXT);'
    try: 
        cursor.execute(query)
        print('Table', tableName, 'has been created in the DB')
    except sqlite3.Error as error:
        print("Failed to create table in the DB", error)
    finally:
        cursor.close() 
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
                _id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE
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

def insert_table(conn,tableName, colNames, r):
    cursor = conn.cursor()
    # recording in the table result
    query = """
        INSERT INTO {tab}(""".format(tab = tableName)
    for c in colNames:
        if c != colNames[-1]: 
            query = query + c + ', '
        else:
            query = query + c + ') VALUES ('
            for l in colNames:
                if l != colNames[-1]:
                    query = query + '?, '
                else:
                    query = query + '?);'
    try: 
        cursor.execute(query, r)
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)

def write_csv(pathname, fileName, colName, data):
    """
    Write data in a CSV file
    pathname [str] : folder location of the csv file 
    fileName [str] : name of the csv file
    colName [str] : name of the columns
    data [dictionary]: data to be recorded
    """
    csv_file = os.path.join(pathname,fileName)
    try:
        if not os.path.isfile(csv_file):
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(colName)
            print(fileName, ' has been created in : ', pathname) 
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for k, v in data.items():
                r = list(k)
                r.append(v)
                writer.writerow(r)
    except IOError:
        print("I/O error")
