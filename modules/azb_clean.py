from .azb_repository import AzbRepository
from .logger import log
from .utils import is_directory
from .azb_settings import get_azb_settings

import os
import re
from datetime import datetime

ZIP_FILENAME_PATTERN = re.compile(r"^(.+)_azb_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.\d+)\.zip$")

class ZipFile:
  def __init__(self, file_name, file_path, filename_datetime, created_datetime, to_delete):
    self.file_name         = file_name
    self.file_path         = file_path
    self.filename_datetime = filename_datetime
    self.created_datetime  = created_datetime
    self.to_delete         = to_delete

def clean_directory(dir_path, num_zips_to_keep):
  if not is_directory(dir_path):
      log("  Directory not found")
      return

  all_files = os.listdir(dir_path)

  zip_files = []

  for file_name in all_files:
    match = ZIP_FILENAME_PATTERN.match(file_name)
    if not match:
      log(f"  Unexpected file found: '{file_name}'")
      log(f"  Skipping directory")
      return
    
    datetime_str = match.group(2)
    file_path = os.path.join(dir_path, file_name)
    created_datetime = datetime.fromtimestamp(os.path.getmtime(file_path))
    filename_datetime = datetime.strptime(datetime_str, "%Y-%m-%d-%H-%M-%S.%f")
    zip_files.append(ZipFile(
      file_name=file_name,
      file_path=file_path,
      filename_datetime=filename_datetime,
      created_datetime=created_datetime,
      to_delete=False
    ))

  zip_files.sort(key=lambda e: e.filename_datetime)

  for i in range(1, len(zip_files)):
    if zip_files[i].created_datetime < zip_files[i - 1].created_datetime:
      log("  File creation date order does not match file name order")
      log("  Skipping directory")
      return
  
  if len(zip_files) > num_zips_to_keep:
    for zip_file in zip_files[:-num_zips_to_keep]:
      zip_file.to_delete = True

  log(f"  Files in directory (oldest to newest):")
  for zip_file in zip_files:
    label = f"{zip_file.created_datetime.strftime('%Y-%m-%d %H:%M:%S')}  {zip_file.file_name}"
    if zip_file.to_delete:
      log(f"    [DELETE]  {label}")
    else:
      log(f"    [KEEP]    {label}")
  
  if not any(e.to_delete for e in zip_files):
    log("  Nothing to delete")
    return
  
  answer = input("  Delete marked files? (Y/N): ").strip().upper()
  if answer != "Y":
    log("  Skipping directory")
    return
  
  for zip_file in zip_files:
    if zip_file.to_delete:
      os.remove(zip_file.file_path)
      log(f"    Deleted {os.path.basename(zip_file.file_path)}")

  for zip_file in zip_files:
    if not zip_file.to_delete and not os.path.exists(zip_file.file_path):
      log(f"    WARNING: Expected file missing after deletion: {zip_file.file_path}")


def run_clean():
  azb_repository = AzbRepository()
  dir_destination_models = azb_repository.get_all_dir_destination_models()

  num_zips_to_keep = get_azb_settings().get("clean", {}).get("keepRecentZipsPerDirectory")
  
  if num_zips_to_keep is None:
    raise ValueError("clean.keepRecentZipsPerDirectory is not set in azb_settings.json")
  
  log(f"Number of zip files to keep, per directory: {num_zips_to_keep}")

  for i, dir_destination_model in enumerate(dir_destination_models, start=1):
    log("")
    log(f"Destination directory location {i} of {len(dir_destination_models)}: {dir_destination_model.dir_path}")
    
    clean_directory(dir_destination_model.dir_path, num_zips_to_keep)
