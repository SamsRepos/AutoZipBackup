import json
import sqlite3
from db_connection import create_connection
from dir_hasher import hash_dir

SETTINGS_FILE_PATH = "./azb_settings.json"

DB_PATH_KEY = "dbPath"

def db_path():
  with open(SETTINGS_FILE_PATH) as json_file:
    json_data = json.load(json_file)
    if DB_PATH_KEY in json_data:
      return json_data[DB_PATH_KEY]

db = create_connection(db_path())

c = db.cursor()
c.row_factory = sqlite3.Row

rows = c.execute("SELECT * FROM dirs_to_hash")
for row in rows:
  dir_path = row["dir_path"]
  print(f"Hashing directory at {dir_path}")
  hash = hash_dir(dir_path)
  data = ( dir_path, hash )
  print(f"hash: {hash}")
  c.execute("INSERT INTO dir_hashes (dir_path, hash) VALUES (?, ?)", data)