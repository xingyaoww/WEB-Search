import sqlite3
import os
from pack import config
dbname = config.dbname


def db_init(dbname):
    print(f'* Database Initialization Started - {dbname}')
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


# try:
#     cur.execute('SELECT * FROM sqlite_sequence')
#     if cur is not None: print('** Database Exists **')
#     else:print('** Creating New Tables in db. **')
# except: print('Brand New DB.')
# cur.executescript('''
# CREATE TABLE IF NOT EXISTS Dirs(
#     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE ,
#     dir TEXT UNIQUE ,
#     status INTEGER ,
#     size INTEGER
# )''')
# # status: 0 means directory, 1 means file, -1 means error;
# # size: represent in byte
# print('* Database Initialization Completed')

def check_db(cur=cur):
    tempcur = cur.execute('SELECT * FROM sqlite_sequence ')
    if tempcur is not None:
        print('Exist Tables:')
        for x in tempcur:print(f'  >name:{x[0]} seq:{x[1]}')

        
def renew_db(cur=cur):
    conn.commit()
    cur.close()
    os.remove(dbname)
    db_init(cur)
    print('Database Renewed')