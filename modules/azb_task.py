from datetime import datetime
import os
import shutil

from .logger import log

class AzbTask:
  def __init__(self, dir_source_model, dir_destination_models, source_current_hash):
    self.dir_source_model       = dir_source_model
    self.dir_destination_models = dir_destination_models
    self.source_current_hash    = source_current_hash
    
    self.task_name = dir_source_model.task_name
    self.dir_path  = dir_source_model.dir_path
    self.destination_paths = [d.dir_path for d in dir_destination_models]

  def run(self):
    log(f"  Zipping and copying now...")

    num_destinations = len(self.destination_paths)

    # 3. Compressing
    log(f"  - {num_destinations} destination location" + ("s" if num_destinations > 1 else "") + ": ")
    for path in self.destination_paths:
      log(f"    - {path}")

    datetime_for_file_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
    zip_file_name = f"{self.task_name}_azb_{datetime_for_file_name}"

    # Compressing to first destination

    zipping_destination_path = self.destination_paths[0]
    zipping_file_path = os.path.join(zipping_destination_path, zip_file_name)
    log(f"  - Preparing to create zip at " + ("first" if num_destinations > 1 else "") + f" directory: {zipping_destination_path}")
    log(f"    - Zip file name: {zip_file_name}.zip")
    log(f"    - Zipping now...")
    shutil.make_archive(zipping_file_path, 'zip', self.dir_path, verbose=True)
    log(f"    - Zip complete: {zipping_file_path}")
    
    zipped_file_path = zipping_file_path + ".zip"

    # Copying zip to any other destinations
    if num_destinations > 1:
      for i in range(len(self.destination_paths)):
        if i == 0:
          continue
        destination_path = self.destination_paths[i]
        log(f"  - Preparing to copy {zipped_file_path}")
        log(f"    - Destination: {destination_path}")
        log(f"    - Copying now...")
        shutil.copy(zipped_file_path, destination_path)
        log(f"    - Copy complete")

    log(f"Auto zip backup task complete: {self.task_name}")
    log("")

  def save_hash(self):
    
    self.dir_source_model.latest_hash = self.source_current_hash
    self.dir_source_model.save()

    for dir_destination_model in self.dir_destination_models:
      dir_destination_model.latest_source_hash = self.source_current_hash
      dir_destination_model.save()