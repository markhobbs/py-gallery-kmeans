# init.py

import config
import sqlite3, os
from sqlite3 import Error

# DELETE OLD DB IF EXIST
# if os.path.exists(config.filepaths['dbfile']):
#   os.remove(config.filepaths['dbfile'])

try:
    conn = sqlite3.connect(config.filepaths['dbfile'])
    with open(config.filepaths['SQLFILE']) as f:
      conn.executescript(f.read())
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if conn:
        conn.commit()
        conn.close()
        print("Database Created, The SQLite connection is closed")
