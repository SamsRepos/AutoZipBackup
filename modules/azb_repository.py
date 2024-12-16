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
      i += 1
      log(f"Updating source hash for destination dir {i} of {len(dir_destination_models)}: {dir_destination_model.dir_path}")
      data = (new_hash, dir_destination_model.id)
      db_cursor.execute("UPDATE dir_destination SET latest_source_hash=? WHERE id=?", data)
      db.commit()

    log("")

  def save_dir_source(self, dir_source_model):
    db_cursor = self.get_db_cursor()
    
    if not hasattr(dir_source_model, 'id') or dir_source_model.id is None:
      data = (
        dir_source_model.task_name,
        dir_source_model.dir_path,
        dir_source_model.task_active,
        dir_source_model.latest_hash
      )
      db_cursor.execute("""
        INSERT INTO dir_source (task_name, dir_path, active, latest_hash)
        VALUES (?, ?, ?, ?)
      """, data)
      dir_source_model.id = db_cursor.lastrowid
    else:
      data = (
        dir_source_model.task_name,
        dir_source_model.dir_path,
        dir_source_model.task_active,
        dir_source_model.latest_hash,
        dir_source_model.id
      )
      db_cursor.execute("""
        UPDATE dir_source 
        SET task_name=?, dir_path=?, active=?, latest_hash=?
        WHERE id=?
      """, data)

    self.db.commit()
    db_cursor.close()
    return dir_source_model

  def save_dir_destination(self, dir_destination_model):
    db_cursor = self.get_db_cursor()
    
    data = (dir_destination_model.dir_source_id,)
    source_exists = db_cursor.execute(
      "SELECT 1 FROM dir_source WHERE id=?", data
    ).fetchone()
    
    if not source_exists:
      raise ValueError(f"Source directory with id {dir_destination_model.dir_source_id} does not exist")

    if not hasattr(dir_destination_model, 'id') or dir_destination_model.id is None:
      data = (
        dir_destination_model.dir_source_id,
        dir_destination_model.dir_path,
        dir_destination_model.active,
        dir_destination_model.latest_source_hash
      )
      db_cursor.execute("""
        INSERT INTO dir_destination (dir_source_id, dir_path, active, latest_source_hash)
        VALUES (?, ?, ?, ?)
      """, data)
      dir_destination_model.id = db_cursor.lastrowid
    else:
      data = (
        dir_destination_model.dir_source_id,
        dir_destination_model.dir_path,
        dir_destination_model.active,
        dir_destination_model.latest_source_hash,
        dir_destination_model.id
      )
      db_cursor.execute("""
        UPDATE dir_destination 
        SET dir_source_id=?, dir_path=?, active=?, latest_source_hash=?
        WHERE id=?
      """, data)

    self.db.commit()
    db_cursor.close()
    return dir_destination_model

  def update_source_task_name(self, source_id, new_task_name):
      db_cursor = self.get_db_cursor()
      data = (new_task_name, source_id)
      db_cursor.execute("UPDATE dir_source SET task_name=? WHERE id=?", data)
      self.db.commit()
      db_cursor.close()

  def update_source_dir_path(self, source_id, new_dir_path):
      db_cursor = self.get_db_cursor()
      data = (new_dir_path, source_id)
      db_cursor.execute("UPDATE dir_source SET dir_path=? WHERE id=?", data)
      self.db.commit()
      db_cursor.close()

  def update_destination_dir_path(self, destination_id, new_dir_path):
      db_cursor = self.get_db_cursor()
      data = (new_dir_path, destination_id)
      db_cursor.execute("UPDATE dir_destination SET dir_path=? WHERE id=?", data)
      self.db.commit()
      db_cursor.close()
