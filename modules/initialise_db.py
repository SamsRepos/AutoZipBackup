import sqlite3
from modules.azb_settings import get_azb_settings

SQL_PATH = "./tables.sql" ## fine as is

def initialise_db():
    db_path = get_azb_settings().get("dbPath")
    with open(SQL_PATH) as f:
        sql = f.read()
    conn = sqlite3.connect(db_path)
    conn.executescript(sql)
    conn.close()
    print("Database initialised")
