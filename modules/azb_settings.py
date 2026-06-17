import json

SETTINGS_FILE_PATH = "./azb_settings.json"

def get_azb_settings():
  with open(SETTINGS_FILE_PATH) as json_file:
    return json.load(json_file)