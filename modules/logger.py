import os
from datetime import datetime

from .utils import is_directory, datetime_formatted

__LOG_DIR_NAME__ = "log"
__LOG_DIR_RELATIVE_PATH__ = f"./{__LOG_DIR_NAME__}/"

if not is_directory(__LOG_DIR_RELATIVE_PATH__):
  os.mkdir(__LOG_DIR_NAME__)

__log_file_name__ = f"azb_log_{datetime.now()}.log".replace(" ", "-").replace(":", "-")
__log_file_path__ = os.path.abspath(__LOG_DIR_RELATIVE_PATH__)
__log_file_path__ = os.path.join(__log_file_path__, __log_file_name__)



def log(message):
  print(message)
  with open(__log_file_path__, "a") as log_f:
    now_str = datetime_formatted(datetime.now())
    log_str = f"{now_str}: {message}"
    log_f.write(log_str)
    log_f.write('\n')