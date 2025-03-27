import sqlite3
from flask import g

def connect_database():
    database = sqlite3.connect("database.db")
    database.execute("PRAGMA foreign_keys = ON")
    database.row_factory = sqlite3.Row
    return database

def execute(sql, parameters=[]):
    database = connect_database()
    result = database.execute(sql, parameters)
    database.commit
    g.last_insert_id = result.lastrowid
    database.close()

def last_insert_id():
    return g.last_insert_id

def query(sql, parameters=[]):
    database = connect_database()
    result = execute(sql, parameters).fetchall()
    database.close()
    return result