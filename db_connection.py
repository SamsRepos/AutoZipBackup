import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print(f"Connected to SQLite Db at \"{path}\"")
    except Error as e:
        print(f"Error connecting to SQLite: {e}")

    return connection