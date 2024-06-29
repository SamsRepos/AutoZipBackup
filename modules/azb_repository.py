import sqlite3

from .db_connection import get_default_db_connection

from .models.dir_source_model import DirSourceModel
from .models.dir_destination_model import DirDestinationModel

from .logger import log

class AzbRepository:
  def __init__(self):
    self.db = get_default_db_connection()

  def get_db_cursor(self):
    db_cursor = self.db.cursor()
    db_cursor.row_factory = sqlite3.Row
    return db_cursor

  def get_all_dir_source_models(self):
    db_cursor = self.get_db_cursor()
    rows = db_cursor.execute("SELECT * FROM dir_source").fetchall()
    
    res = []

    for row in rows:
      res.append(DirSourceModel(row))

    db_cursor.close()

    return res

  def get_dir_destination_models(self, dir_source_id):
    db_cursor = self.get_db_cursor()
    data = (dir_source_id,)
    rows = db_cursor.execute("""
      SElECT * FROM dir_destination
      WHERE dir_source_id=?    
    """, data).fetchall()

    res = []

    for row in rows:
      res.append(DirDestinationModel(row))

    db_cursor.close()

    return res
  
  def save_new_hash(self, dir_source_model, dir_destination_models, new_hash):
    db = self.db
    db_cursor = self.get_db_cursor()

    if new_hash != dir_source_model.latest_hash:
      log(f"Updating hash for source dir {dir_source_model.dir_path}")
      data = (new_hash, dir_source_model.id)
      db_cursor.execute("UPDATE dir_source SET latest_hash=? WHERE id=?", data)
      db.commit()

    i = 0
    for dir_destination_model in dir_destination_models:
      log(f"Updating source hash for destination dir {i} of {len(dir_destination_models)}: {dir_source_model.dir_path}")
      data = (new_hash, dir_destination_model.id)
      db_cursor.execute("UPDATE dir_destination SET latest_source_hash=? WHERE id=?", data)
      db.commit()

      i += 1

    log("")

