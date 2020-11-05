''' Copyright FERAMS : 2020 '''

# Importing Packages
import sqlite3

# Initialising the SQLite Database
def InitialiseDatabase():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id integer unique primary key autoincrement,
        roll_no text);"""
    c.executescript(sql)
    conn.commit()
    conn.close()
