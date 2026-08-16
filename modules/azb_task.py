from datetime import datetime
import os
import shutil
import zipfile
from .azb_settings import get_azb_settings

from .logger import log

class AzbTask:
  def __init__(self, dir_source_model, dir_destination_models, source_current_hash):
    self.dir_source_model       = dir_source_model
    self.dir_destination_models = dir_destination_models
    self.source_current_hash    = source_current_hash
    
    self.task_name = dir_source_model.task_name
    self.source_path  = dir_source_model.dir_path
    self.destination_paths = [d.dir_path for d in dir_destination_models]

  def run(self):
    log(f"  Running azb_task: {self.task_name}")

    num_destinations = len(self.destination_paths)

    # 3. Compressing
    log(f"  - source location: {self.source_path}")
    log(f"  - {num_destinations} destination location" + ("s" if num_destinations > 1 else "") + ": ")
    for path in self.destination_paths:
      log(f"    - {path}")

    datetime_for_file_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
    zip_file_name = f"{self.task_name}_azb_{datetime_for_file_name}.zip"

    # Compressing to first destination
    zipping_destination_path = self.destination_paths[0]
    zip_file_path = os.path.join(zipping_destination_path, zip_file_name)
    log(f"  - Preparing to create zip at" + (" first" if num_destinations > 1 else "") + f" directory: {zipping_destination_path}")
    log(f"    - Zip file name: {zip_file_name}")
    log(f"    - Zipping now...")

    ignore_extensions = set(get_azb_settings().get("ignoreFileExtensions", []))
    with zipfile.ZipFile(
      file=zip_file_path,
      mode='w',
      compression=zipfile.ZIP_DEFLATED
    ) as zf:
      for root, dirs, files in os.walk(self.source_path):
        for file in files:
          if os.path.splitext(file)[1].lower() in ignore_extensions:
            continue
          file_path = os.path.join(root, file)
          arcname = os.path.relpath(
            path=file_path,
            start=self.source_path
          )
          zf.write(
            filename=file_path,
            arcname=arcname
          )

    log(f"    - Zip complete: {zip_file_path}")

    # Copying zip to any other destinations
    if num_destinations > 1:
      for i in range(len(self.destination_paths)):
        if i == 0:
          continue
        destination_path = self.destination_paths[i]
        log(f"  - Preparing to copy {zip_file_path}")
        log(f"    - Destination: {destination_path}")
        log(f"    - Copying now...")
        shutil.copy(zip_file_path, destination_path)
        log(f"    - Copy complete")

    log(f"  azb_task complete: {self.task_name}")
    log("")
