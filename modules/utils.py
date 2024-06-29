from datetime import datetime, timedelta
from time import sleep
import os

def sleep_until(hour, minute):
  today = datetime.today()
  future = datetime(today.year, today.month, today.day, hour, minute)
  if today.timestamp() > future.timestamp():
    future += timedelta(days=1)
  sleep((future - today).total_seconds())

def today_string():
  today = datetime.today()
  return f"{today.year}-{today.month}-{today.day}"

def time_string(hour, minute):
  return "%02d:%02d" % (hour, minute)

def datetime_formatted(dt):
  return dt.strftime('%H:%M:%S %d/%m/%Y')

def is_directory(path):
   return os.path.isdir(path)