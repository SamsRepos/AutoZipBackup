from .azb_task import AzbTask
from .logger import log
from .dir_hasher import hash_dir

from .models.dir_source_model import DirSourceModel
from .models.dir_destination_model import DirDestinationModel
from .azb_repository import AzbRepository

import os

def is_dir(path):
   return os.path.isdir(path)

def create_azb_task(dir_source_model):
  log("")

  log(f"  task_name: {dir_source_model.task_name}")
  
  log(f"  source directory path: {dir_source_model.dir_path}")
  if not is_dir(dir_source_model.dir_path):
    log("  Directory not found.")
    log("  Skipping this profile.")
    log("")
    return None
  
  log(f"  active: {dir_source_model.task_active != 0}")
  if not dir_source_model.task_active:
      log("  Skipping this profile.")
      log("")
      return None
  
  log(f"  latest hash: {dir_source_model.latest_hash}")

  log("  Hashing now...")
  source_current_hash = hash_dir(dir_source_model.dir_path)
  log(f"  current hash: {source_current_hash}")

  if source_current_hash != dir_source_model.latest_hash:
    log("  Source directory contents has changed.")

  azb_repository = AzbRepository()
  dir_destination_models_found = azb_repository.get_dir_destination_models(dir_source_model.id)
  
  dir_destination_models_for_task = []

  i = 0
  for dir_destination_model in dir_destination_models_found:
    log("")
    
    log(f"  Destination {i+1} of {len(dir_destination_models_found)}:")
    
    log(f"    destination directory path: {dir_destination_model.dir_path}")
    if not is_dir(dir_destination_model.dir_path):
      log("    Directory not found.")
      log("    Skipping this destination directory.")
      continue
    
    log(f"    active: {dir_destination_model.active != 0}")
    if not dir_destination_model.active:
      log("    Skipping this destination directory.")
      continue

    log(f"    destination directory's latest source hash: {dir_destination_model.latest_source_hash}")

    if dir_destination_model.latest_source_hash != dir_source_model.latest_hash:
      log("    Destination directory is behind.")
    
    if dir_destination_model.latest_source_hash == source_current_hash:
      log("    Destination directory has already recieved an up-to-date backup :)")
    else:
      log("    Adding destination path to task.")
      dir_destination_models_for_task.append(dir_destination_model)

    i += 1

  log("")

  if len(dir_destination_models_for_task) < 1:
     log("  Skipping this profile.")
     return None

  destination_paths_chained = ", ".join([d.dir_path for d in dir_destination_models_for_task])
  log(f"  Proceeding with {len(dir_destination_models_for_task)} of {len(dir_destination_models_found)} destination paths: {destination_paths_chained}")
  
  return AzbTask(dir_source_model, dir_destination_models_for_task, source_current_hash)