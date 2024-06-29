import json
import sqlite3
from sqlite3 import Error

from .logger import log

SETTINGS_FILE_PATH = "./azb_settings.json"

DB_PATH_KEY = "dbPath"

def db_path():
  with open(SETTINGS_FILE_PATH) as json_file:
    json_data = json.load(json_file)
    if DB_PATH_KEY in json_data:
      return json_data[DB_PATH_KEY]

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