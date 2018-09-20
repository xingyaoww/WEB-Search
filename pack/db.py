import sqlite3
import os
from pack.config import *

def db_init(dbname=default_dbname):
    print(f'* Database Initialization Started - {dbname} \n')
    global conn
    conn = sqlite3.connect(dbname)
    global cur
    cur = conn.cursor()
    # Page Table
    cur.execute('''CREATE TABLE IF NOT EXISTS Pages(
        id INTEGER PRIMARY KEY, 
        url TEXT UNIQUE, 
        html TEXT,
        error INTEGER, 
        old_rank REAL, 
        new_rank REAL
        )''')

    # Intermediate Table-Links
    cur.execute('''CREATE TABLE IF NOT EXISTS Links(
        from_id INTEGER, 
        to_id INTEGER
        )''')

    # Web Table Stores URL
    cur.execute('''CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE)''')
    return cur,conn
def renew_db(cur,conn,dbname=default_dbname):
    conn.commit()
    cur.close()
    os.remove(dbname)
    db_init()
    print('Database Renewed')