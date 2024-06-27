import json
import sqlite3
from .db_connection import create_connection
from .dir_hasher import hash_dir

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

  db = create_connection(db_path())

  c = db.cursor()
  c.row_factory = sqlite3.Row

  rows = c.execute("SELECT * FROM dirs").fetchall()

  i = 0
  for row in rows:
    id = row["id"]
    dir_path = row["dir_path"]
    active = row["active"]
    destination_paths = json.loads(row["destination_paths"])
    latest_hash = row["latest_hash"]

    log("")
    log(f"dir {i+1} of {len(rows)}: {dir_path}")
    log(f"  active: {active != 0}")
    if not active:
      log("  Skipping.")
      log("")
      continue

    destination_paths_chained = ", ".join(destination_paths)

    log(f"  destination paths: {destination_paths_chained}")
    log(f"  latest hash: {latest_hash}")

    log("  Hashing now...")
    current_hash = hash_dir(dir_path)
    log(f"  current hash: {current_hash}")
    
    if current_hash == latest_hash:
      log("  Skipping.")
      log("")
      continue

    log("  [TODO: ziping and copying now]")

    data = ( current_hash, id )
    c.execute("UPDATE dirs SET latest_hash=? WHERE id=?", data)
    #c.execute(f"UPDATE dirs SET latest_hash='{current_hash}' WHERE id={id}")
    db.commit()

    i += 1

      # from example:
      # c.execute("INSERT INTO dir_hashes (dir_path, hash) VALUES (?, ?)", data)

  c.close()





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

# class AzbTask:
#   def __init__(self, name, dir_path, zip_destination_paths):
#     self.name     = name
#     self.dir_path = dir_path
#     self.destination_paths = zip_destination_paths

#   def run(self):
#     print(f"Running azb task: {self.name}")

#     num_destinations = len(self.destination_paths)

#     print(f" - Directory: {self.dir_path}")
#     # 1. Check if task has been run for this directory before:
#     if dir_in_history(self.dir_path):
#       # 2. Check if there have been any changes since last run:  
#       print(f" - Checking for changes...")
#       if dir_changed(self.dir_path):
#         print(f" - Changes found. Proceeding with azb...")
#       else:
#         print(f" - No changes found. Exiting task now: {self.name}")
#         print()
#         return      
#     else:
#       print(f" - Running for the first time on this directory")
#       add_dir_column(self.dir_path)

#     # 3. Compressing
#     print(f" - {num_destinations} destination location" + ("s" if num_destinations > 1 else "") + ": ")
#     for path in self.destination_paths:
#       print(f"   - {path}")

#     datetime_for_file_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
#     zip_file_name = f"{self.name}_auto_zip_backup_{datetime_for_file_name}"

#     zipping_destination_path = self.destination_paths[0]
#     zipping_file_path = os.path.join(zipping_destination_path, zip_file_name)
#     print(f" - Preparing to create zip at " + ("first" if num_destinations > 1 else "") + f" directory: {zipping_destination_path}")
#     print(f"   - Zip file name: {zip_file_name}.zip")
#     print(f"   - Zipping now...")
#     shutil.make_archive(zipping_file_path, 'zip', self.dir_path, verbose=True)
#     print(f"   - Zip complete: {zipping_file_path}")
    
#     zipped_file_path = zipping_file_path + ".zip"

#     # 4. Copying zip to any other destinations
#     if num_destinations > 1:
#       for i in range(len(self.destination_paths)):
#         if i == 0:
#           continue
#         destination_path = self.destination_paths[i]
#         print(f" - Preparing to copy {zipped_file_path}")
#         print(f"   - Destination: {destination_path}")
#         print(f"   - Copying now...")
#         shutil.copy(zipped_file_path, destination_path)
#         print(f"   - Copy complete")

#     print(f"Auto zip backup task complete: {self.name}")
#     print()


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
  