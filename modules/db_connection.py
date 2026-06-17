import json
import sqlite3
from sqlite3 import Error
from .logger import log
from .azb_settings import get_azb_settings

DB_PATH_KEY = "dbPath"

def db_path():
  return get_azb_settings().get(DB_PATH_KEY)

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        #log(f"[Connected to SQLite Db at \"{path}\"]")
    except Error as e:
        log(f"[Error connecting to SQLite: {e}]")

    return connection

def get_default_db_connection():
   return create_connection(db_path())