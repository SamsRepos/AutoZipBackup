import json
import sqlite3
from .db_connection import create_connection
from .dir_hasher import hash_dir
from .azb_task import AzbTask

SETTINGS_FILE_PATH = "./azb_settings.json"

DB_PATH_KEY = "dbPath"

def log(str):
  print(str)

def db_path():
  with open(SETTINGS_FILE_PATH) as json_file:
    json_data = json.load(json_file)
    if DB_PATH_KEY in json_data:
      return json_data[DB_PATH_KEY]

def run_azb():

  azb_tasks = []

  db = create_connection(db_path())

  c = db.cursor()
  c.row_factory = sqlite3.Row

  rows = c.execute("SELECT * FROM dirs").fetchall()

  i = 0
  for row in rows:
    id                = row["id"]
    task_name         = row["task_name"]
    dir_path          = row["dir_path"]
    active            = row["active"]
    destination_paths = json.loads(row["destination_paths"])
    latest_hash       = row["latest_hash"]

    log("")
    log(f"Loaded {i+1} of {len(rows)}:")
    log(f"  task_name: {task_name}")
    log(f"  active:    {active != 0}")
    if not active:
      log("  Skipping.")
      log("")
      continue

    destination_paths_chained = ", ".join(destination_paths)

    log(f"  dir_path:          {dir_path}") 
    log(f"  destination paths: {destination_paths_chained}")
    log(f"  latest hash:       {latest_hash}")

    log("  Hashing now...")
    current_hash = hash_dir(dir_path)
    log(f"  current hash: {current_hash}")
    
    if current_hash == latest_hash:
      log("  Skipping.")
      log("")
      continue

    # TODO - check to ensure directories all exist
    #      - if some output dirs don't exist
    #          warn and proceed on existing dirs
    #      - else exclude task

    data = ( current_hash, id )
    c.execute("UPDATE dirs SET latest_hash=? WHERE id=?", data)
    db.commit()

    log(f"  Adding task {task_name} to azb_tasks")
    task = AzbTask(task_name, dir_path, destination_paths)
    azb_tasks.append(task)

    i += 1

  c.close()

  log("")
  log(f"{len(azb_tasks)} of {len(rows)} directories changed")
  log("Running AZB tasks...")
  i = 0
  for task in azb_tasks:
    log(f"  Running task {i+1} of {len(azb_tasks)} ...")
    task.run()
    i += 1





# import shutil
# import json
# from datetime import datetime
# import os
# import pandas

# from modules.utils import sleep_until, today_string, time_string
# from modules.dir_hasher import hash_dir

# JSON_FILE_PATH = r".\azb_tasks.json"

# JSON_AZB_TASKS_RUN_TIME   = 'run_time'           # array of two numbers: [hh, mm]

# JSON_AZB_TASKS_NAME       = "azb_tasks"          # string
# JSON_AZB_NAME_KEY         = 'name'               # string
# JSON_AZB_DIR_PATH_KEY     = 'dir_path'           # string
# JSON_AZB_DESTINATIONS_KEY = 'destination_paths'  # array of strings

# azb_tasks = []

# run_hour    = 00
# run__minute = 00

# CSV_FILE_PATH =  r".\azb_hashes.csv"

# CSV_DATE_COLUMN_NAME = "date"

# def get_hashes_df():
#   with open(CSV_FILE_PATH) as csv_file:
#     return pandas.read_csv(csv_file, skipinitialspace=True)

# def write_to_csv(data_frame):
#   data_frame.to_csv(CSV_FILE_PATH, index=False)

# def already_ran_tasks_today():
#   data_frame = get_hashes_df()
#   key = data_frame[CSV_DATE_COLUMN_NAME] == today_string()
#   matching_rows = data_frame[key]
#   return (len(matching_rows) > 0)

# def dir_in_history(dir_path):
#   data_frame = get_hashes_df()
#   return (dir_path in data_frame)

# def dir_changed(dir_path):
#   data_frame = get_hashes_df()
#   hashes = list(data_frame[dir_path])
#   most_recent_hash = hashes[-1]
#   print(f"   - Most recent hash: {most_recent_hash}")
#   print(f"   - Hashing now...")
#   current_hash = hash_dir(dir_path)
#   print(f"   - Current hash: {current_hash}")
#   if most_recent_hash == current_hash:
#     return False
#   else:
#     print(f"   - Writing new hash to {CSV_FILE_PATH}")
#     data_frame.at[(len(data_frame.index)-1), dir_path] = current_hash
#     write_to_csv(data_frame)
#     return True

# def add_today_row():
#   data_frame = get_hashes_df()
#   new_row = [ today_string() ]
#   for i in (range(len(list(data_frame.columns)) - 1)):
#     new_row.append('')
#   data_frame.loc[len(data_frame.index)] = new_row
#   write_to_csv(data_frame)

# def add_dir_column(dir_path):
#   data_frame = get_hashes_df()
#   new_column_pos = len(list(data_frame.columns))
#   empties = []
#   for i in range(len(data_frame.index)):
#     empties.append('')
#   data_frame.insert(new_column_pos, dir_path, empties)
#   write_to_csv(data_frame)



# def load_azb_tasks():
#   with open(JSON_FILE_PATH) as json_file:
#     json_data = json.load(json_file)
#     if JSON_AZB_TASKS_RUN_TIME in json_data:
#       global run_hour, run__minute
#       run_hour    = json_data[JSON_AZB_TASKS_RUN_TIME][0]
#       run__minute = json_data[JSON_AZB_TASKS_RUN_TIME][1]
#     for task_data in json_data[JSON_AZB_TASKS_NAME]:
#       task = AzbTask(
#         name                  = task_data[JSON_AZB_NAME_KEY],
#         dir_path              = task_data[JSON_AZB_DIR_PATH_KEY],
#         zip_destination_paths = task_data[JSON_AZB_DESTINATIONS_KEY]
#       )
#       azb_tasks.append(task)



# if __name__ == '__main__':
#   load_azb_tasks()

#   while True:
#     if already_ran_tasks_today():
#       print(f"Already ran AZB tasks today. Waiting until {time_string(run_hour, run__minute)}")
#       sleep_until(run_hour, run__minute)
#     add_today_row()
#     for task in azb_tasks:
#       task.run()
  