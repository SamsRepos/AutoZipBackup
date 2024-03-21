import shutil
import json
from datetime import datetime
import os

class AzbTask:
  def __init__(self, name, dir_path, zip_destination_paths):
    self.name     = name
    self.dir_path = dir_path
    self.destination_paths = zip_destination_paths

  def run(self):
    print(f"Running auto zip backup task: {self.name}")

    num_destinations = len(self.destination_paths)

    print(f" - Directory to compress: {self.dir_path}")
    print(f" - {num_destinations} destination location" + ("s" if num_destinations > 1 else "") + ": ")
    for path in self.destination_paths:
      print(f"   - {path}")

    datetime_for_file_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
    zip_file_name = f"{self.name}_auto_zip_backup_{datetime_for_file_name}"

    zipping_destination_path = self.destination_paths[0]
    zipping_file_path = os.path.join(zipping_destination_path, zip_file_name)
    print(f" - Preparing to create zip at " + ("first" if num_destinations > 1 else "") + f" directory: {zipping_destination_path}")
    print(f" - Zip file name: {zip_file_name}")
    print(f"  - Zipping now...")
    shutil.make_archive(zipping_file_path, 'zip', self.dir_path, verbose=True)
    print(f"  - Zip complete: {zipping_file_path}")
    
    zipped_file_path = zipping_file_path + ".zip"

    if num_destinations > 1:
      for i in range(len(self.destination_paths)):
        if i == 0:
          continue
        destination_path = self.destination_paths[i]
        print(f" - Preparing to copy {zipped_file_path}")
        print(f"  - Destination: {destination_path}")
        print(f" - Copying now...")
        shutil.copy(zipped_file_path, destination_path)
        print(f" - Copy complete")
    
    print(f"Auto zip backup task complete: {self.name}")


JSON_AZB_TASKS_NAME       = "azb_tasks"          # string
JSON_AZB_NAME_KEY         = 'name'               # string
JSON_AZB_DIR_PATH_KEY     = 'dir_path'           # string
JSON_AZB_DESTINATIONS_KEY = 'destination_paths'  # array

def load_get_azb_tasks():
  azb_tasks = []
  with open(r".\azb_tasks.json") as tasks_json_file:
    tasks_data = json.load(tasks_json_file)
    for task_data in tasks_data[JSON_AZB_TASKS_NAME]:
      task = AzbTask(
        name                  = task_data[JSON_AZB_NAME_KEY],
        dir_path              = task_data[JSON_AZB_DIR_PATH_KEY],
        zip_destination_paths = task_data[JSON_AZB_DESTINATIONS_KEY]
      )
      azb_tasks.append(task)
  return azb_tasks

if __name__ == '__main__':
  azb_tasks = load_get_azb_tasks()

  for task in azb_tasks:
    task.run()
  