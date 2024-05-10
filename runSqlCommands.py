#! /usr/intel/bin/python3.10.8

import sys

sys.path.append('/nfs/site/disks/vmisd_vclp_efficiency/rcg/server/fullServer/venvRcg/lib/python3.11/site-packages')
import UsrIntel.R1


import sqlite3
from optparse import OptionParser
from csv import reader
import re
import json
from ptServerDatabasemysql import *
import code

parser = OptionParser()

parser.add_option("-C", type="string", help="sql command ", dest="cmd")
parser.add_option("-D", type="string", help="database location", dest="dtb")


options, arguments = parser.parse_args()

flag = False
while flag:
    con = sqlite3.connect(options.dtb)
    cur = con.cursor()

    data=cur.execute(options.cmd)
    output = data.fetchall()
    #print(output)

    for row in output:
        print(",".join(map(str, row)))

    #for row in data:
    #    print (row)

    con.commit()
    cur.close()

    #print ("temp")

flag = True
while flag:
    conn = connectMySql()
    cursor = conn.cursor(dictionary=True)
    #SET SQL_SAFE_UPDATES = 0;
    try:
        cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        cursor.execute(options.cmd)
        records = cursor.fetchall()
        #code.interact(local=locals())
        if records:
            #if records[0]['variableValue']:
            if 'records' in locals() and records and isinstance(records, list) and records[0] and 'variableValue' in records[0]:
                for record in records:
                    print(str(record["variableValue"]))
            else:
                for record in records:
                    print(str(record["commandId"])+","+record["command"]+","+record["user"]+","+record["corner"])

                
    except mysql.connector.Error as error:
        print("Error fetching data from MySQL:", error)

    # Closing cursor and connection
    conn.commit()
    conn.close()
    flag = False