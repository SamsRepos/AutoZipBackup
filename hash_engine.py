import json
from db_connection import create_connection

SETTINGS_FILE_PATH = "./azb_settings.json"

DB_PATH_KEY = "dbPath"

def db_path():
  with open(SETTINGS_FILE_PATH) as json_file:
    json_data = json.load(json_file)
    if DB_PATH_KEY in json_data:
      return json_data[DB_PATH_KEY]

db = create_connection(db_path())

c = db.cursor()

res = c.execute("SELECT * FROM dirs_to_hash")

print(res.fetchall())