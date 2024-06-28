from datetime import datetime
import os
import shutil

class AzbTask:
  def __init__(self, task_name, dir_path, zip_destination_paths):
    self.task_name = task_name
    self.dir_path  = dir_path
    self.destination_paths = zip_destination_paths

  def run(self):
    print(f"  Zipping and copying now...")

    num_destinations = len(self.destination_paths)

    # 3. Compressing
    print(f" - {num_destinations} destination location" + ("s" if num_destinations > 1 else "") + ": ")
    for path in self.destination_paths:
      print(f"   - {path}")

    datetime_for_file_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
    zip_file_name = f"{self.task_name}_azb_{datetime_for_file_name}"

    # Compressing to first destination

    zipping_destination_path = self.destination_paths[0]
    zipping_file_path = os.path.join(zipping_destination_path, zip_file_name)
    print(f" - Preparing to create zip at " + ("first" if num_destinations > 1 else "") + f" directory: {zipping_destination_path}")
    print(f"   - Zip file name: {zip_file_name}.zip")
    print(f"   - Zipping now...")
    shutil.make_archive(zipping_file_path, 'zip', self.dir_path, verbose=True)
    print(f"   - Zip complete: {zipping_file_path}")
    
    zipped_file_path = zipping_file_path + ".zip"

    # Copying zip to any other destinations
    if num_destinations > 1:
      for i in range(len(self.destination_paths)):
        if i == 0:
          continue
        destination_path = self.destination_paths[i]
        print(f" - Preparing to copy {zipped_file_path}")
        print(f"   - Destination: {destination_path}")
        print(f"   - Copying now...")
        shutil.copy(zipped_file_path, destination_path)
        print(f"   - Copy complete")

    print(f"Auto zip backup task complete: {self.task_name}")
    print()