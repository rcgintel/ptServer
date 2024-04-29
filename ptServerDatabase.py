#! /usr/intel/bin/python3.10.8
import sys
sys.path.append('/nfs/site/disks/vmisd_vclp_efficiency/rcg/server/fullServer/venvRcg/lib/python3.11/site-packages')
import sqlite3
import configparser
import globalVariable
import os
import code
import time
from rich import print

################### procedures

def create_database(database_name, schema):
    # Connect to SQLite database (will create if not exists)
    conn = sqlite3.connect(database_name)
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Execute the schema SQL statement
    cursor.executescript(schema)
    # Committing changes and closing the connection
    conn.commit()
    conn.close()
    cmd = "chmod 777 "+database_name
    os.system(cmd)
    print(f"Database '{database_name}' created successfully with the given schema.")

################# variable config

def setupDatabase():
    """this proc is for setting up the database
    Schema definition
    commandInputTable = ["commandId","command","user","corner","machineName","serviced","complete","outputLocation"]
    machineTrackerTable = ["machineId","machineName","corner","status","load","commandId"]

    """
    #global ptServerCLI.configFile
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]

    ################ code
    commandInputTable = ["commandId","command","user","corner","machineName","serviced","complete","outputLocation","workWeek"]
    machineTrackerTable = ["machineId","machineName","corner","status","load","commandId","workWeek"]
    userVariablesTable = ["variableId","variableName", "user","variableValue"]

    cmd = """CREATE TABLE IF NOT EXISTS commandInputTable (
        commandId INTEGER PRIMARY KEY,
        command TEXT NOT NULL,
        user TEXT NOT NULL,
        corner TEXT NOT NULL,
        machineName INTEGER,
        serviced INTEGER default 0,
        complete INTEGER default -1,
        outputLocation TEXT,
        workWeek TEXT NOT NULL,
        sectionTop TEXT NOT NULL,
        nameOfBlock TEXT NOT NULL,
        projectName TEXT NOT NULL,
        runTime INTEGER,
        FOREIGN KEY(machineName) REFERENCES machineTrackerTable(machineName)
    );

    CREATE TABLE IF NOT EXISTS machineTrackerTable (
        machineId INTEGER PRIMARY KEY,
        machineName TEXT NOT NULL,
        corner TEXT NOT NULL,
        status TEXT NOT NULL,
        load INTEGER,
        commandId INTEGER,
        workWeek TEXT NOT NULL,
        sectionTop TEXT NOT NULL,
        nameOfBlock TEXT NOT NULL,
        projectName TEXT NOT NULL,
        totalRunTime INTEGER,
        FOREIGN KEY(commandId) REFERENCES commandInputTable(commandId)
    );

    CREATE TABLE IF NOT EXISTS compareInputTable (
        compareId INTEGER PRIMARY KEY,
        commandID INTEGER NOT NULL,
        pathName TEXT NOT NULL,
        comparePoint INTEGER NOT NULL,
        startPoint TEXT NOT NULL,
        endPoint TEXT NOT NULL,
        pinsList TEXT NOT NULL,
        slack TEXT NOT NULL,
        corner TEXT NOT NULL,
        workWeek TEXT NOT NULL,
        sectionTop TEXT NOT NULL,
        nameOfBlock TEXT NOT NULL,
        projectName TEXT NOT NULL
    );

    create table if not exists userVariablesTable (
        variableId INTEGER PRIMARY KEY,
        variableName TEXT NOT NULL,
        user TEXT NOT NULL,
        variableValue TEXT NOT NULL
    );
    
    """

    create_database(databaseLocation,cmd)

def writeToCommandInputTable(command):
    #print(command)
    #global ptServerCLI.configFile
    corner = globalVariable.corner
    user = os.environ['USER']
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]
    conn = sqlite3.connect(databaseLocation)
    cursor = conn.cursor()
    datas = [
        (command, corner, user),
    ]   
    sql = "INSERT INTO commandInputTable (command, corner, user) VALUES (?, ?, ?)"
    #code.interact(local=locals())

    for data in datas:
        id = cursor.execute(sql, data)
    conn.commit()
    conn.close()
    return id.lastrowid

def writeToMachineTrackerTable(dataSql):
    corner = globalVariable.corner
    user = os.environ['USER']
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]
    conn = sqlite3.connect(databaseLocation)
    cursor = conn.cursor()
    sql = "INSERT INTO machineTrackerTable (machineName,corner,status,load,commandId,workWeek) VALUES (?,?,?,?,?,?)"
    #code.interact(local=locals())
    id = cursor.execute(sql, dataSql)
    conn.commit()
    conn.close()
    
def writeToUserVariablesTable(dataSql):
    user = os.environ['USER']
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]
    conn = sqlite3.connect(databaseLocation)
    cursor = conn.cursor()
    #userVariablesTable = ["variableId","variableName", "user","variableValue"]
    sql = "INSERT INTO userVariablesTable (variableName,user,variableValue) VALUES (?,?,?)"
    #code.interact(local=locals())
    id = cursor.execute(sql, dataSql)
    conn.commit()
    conn.close()


def getCompleteFromCommandInputTable(commandId):
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]
    conn = sqlite3.connect(databaseLocation)
    cursor = conn.cursor()
    sqlcmd = "select complete from commandInputTable where commandId = \'"+str(commandId)+"\';"
    flag = 0
    #code.interact(local=locals())
    while flag != 1:
        time.sleep(2)
        #print("Command in wait state")
        cursor.execute(sqlcmd)
        flag = cursor.fetchone()[0]
    sqlcmd = "select outputLocation from commandInputTable where commandId = \'"+str(commandId)+"\';"
    cursor.execute(sqlcmd)
    location = cursor.fetchone()[0]
    conn.close()
    return location



def get_values_from_database(database, table, columns, condition=""):
    try:
        # Connect to the SQLite database in write mode
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        # Construct the SQL query to retrieve the specified columns
        columns_str = ', '.join(columns)
        if condition == "":
            query = f"SELECT {columns_str} FROM {table};"
        else:
            ## here condition should be the eniter where for example
            ## condition = "where serviced = 0"
            query = f"SELECT {columns_str} FROM {table} {condition};"
        #print(query)
        cursor.execute(query)
        # Fetch all the results
        results = cursor.fetchall()
        return results  # Return the fetched results
    except sqlite3.Error as e:
        print("Error retrieving values from database:", e)
        return None
    finally:
        if connection:
            connection.close()  # Close the database connection




def update_field_in_database(database, table, column_to_update, new_value, condition):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        # Construct the SQL query to update the field
        query = f"UPDATE {table} SET {column_to_update} = \'{new_value}\' {condition} ;"
        #print(query)
        cursor.execute(query)
        # Commit the transaction
        connection.commit()
        #print("Field updated successfully.")
    except sqlite3.Error as e:
        print("Error updating field in database:", e)
    finally:
        if connection:
            connection.close()  # Close the database connection



def getAllNotServicedJobs():
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]
    table = "commandInputTable"
    column = ["commandId","corner"]
    condition = "where serviced = 0 "
    sqlOutput = get_values_from_database(databaseLocation,table,column,condition)
    return sqlOutput

#machineTrackerTable = ["machineId","machineName","corner","status","load","commandId","workWeek"]

def getAllAvailbeMachineForCorner(corner):
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]
    table = "machineTrackerTable"
    column = ["machineId","machineName","workWeek"]
    condition = "where status = \'ready\' and corner = \'"+corner+"\' and workWeek = \'"+project+"\'"
    #code.interact(local=locals())
    sqlOutput = get_values_from_database(databaseLocation,table,column,condition)
    return sqlOutput


#commandInputTable = ["commandId","command","user","corner","machineName","serviced","complete","outputLocation","workWeek"]

def updateMachineNameInCommandInputTable(machineName,commandId):
    config = configparser.ConfigParser()
    project = globalVariable.project
    config.read(globalVariable.configFile)
    databaseLocation = config[project]["database"]
    table = "commandInputTable"
    column_to_update = "machineName"
    new_value = machineName
    condition = "where commandId = "+str(commandId)
    #code.interact(local=locals())
    update_field_in_database(databaseLocation, table, column_to_update, new_value, condition)

