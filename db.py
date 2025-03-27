import sqlite3
from flask import g

def connect_database():
    db = sqlite3.connect("database.db")
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row
    return db

def execute():
    db = connect_database()
    result = db.execute(sql, params)
    db.commit
    g.last