import UsrIntel.R1

import mysql.connector

connection_config = {
    "host": "maria3119-lb-ba-in.dbaas.intel.com",
    "port": 3307,
    "user": "rcg_ptServer",
    "password": "Timing123",
    "database": "rcg",
    "tls_versions": ["TLSv1.2", "TLSv1.1"]
}

connection = mysql.connector.connect(**connection_config)
cursor = connection.cursor(dictionary=True)

query = "SELECT VERSION();"
cursor.execute(query)
for row in cursor:
    print (row)

cursor.close()
connection.close()
