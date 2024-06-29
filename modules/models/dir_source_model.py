class DirSourceModel:
  def __init__(self, db_row):
    self.id          = db_row["id"]
    self.task_name   = db_row["task_name"]
    self.dir_path    = db_row["dir_path"]
    self.task_active = db_row["active"]
    self.latest_hash = db_row["latest_hash"]
    