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
