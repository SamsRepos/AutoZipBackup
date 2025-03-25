from .azb_task import AzbTask
from .azb_task_factory import create_azb_task
from .logger import log

from .azb_repository import AzbRepository

def run_azb():

  azb_tasks = []

  azb_repository = AzbRepository()
  dir_source_models = azb_repository.get_all_dir_source_models() 

  for i, dir_source_model in enumerate(dir_source_models, start=1):
    log("")
    log(f"Profile {i} of {len(dir_source_models)}:")

    if not dir_source_model.task_active:
      log(f"  Task {dir_source_model.task_name} is not active. Skipping this profile.")
      log("") 
      continue

    task = create_azb_task(dir_source_model)
    if task:
      log(f"  Adding task {task.task_name} to azb_tasks")
      azb_tasks.append(task)

  

  if(len(azb_tasks) < 1):
    return

  log("")
  log(f"{len(azb_tasks)} of {len(dir_source_models)} tasks set to run.")
  log("Running AZB tasks...")
  i = 0
  for task in azb_tasks:
    log(f"Starting azb_task {i+1} of {len(azb_tasks)}")
    task.run()
    azb_repository.save_new_hash(task.dir_source_model, task.dir_destination_models, task.source_current_hash)
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
  