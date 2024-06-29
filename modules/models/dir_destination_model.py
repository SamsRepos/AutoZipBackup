class DirDestinationModel:
  def __init__(self, db_row):
    self.id                 = db_row["id"]
    self.dir_source_id      = db_row["dir_source_id"]
    self.dir_path           = db_row["dir_path"]
    self.active             = db_row["active"]
    self.latest_source_hash = db_row["latest_source_hash"]
    