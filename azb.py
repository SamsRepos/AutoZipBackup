import argparse
import sys
from time import sleep

from modules.azb_engine import run_azb
from modules.azb_gui import run_gui
from modules.azb_clean import run_clean
from modules.alert import alert
from modules.initialise_db import initialise_db

for i, arg in enumerate(sys.argv):
    print(f"Arg #{i}: {arg}")

class VALID_ARGUMENTS:
  RUN_ONCE = "run_once"
  GUI      = "gui"
  CLEAN    = "clean"
  INIT_DB  = "init_db"
  NO_SOUND = "--no-sound"

parser = argparse.ArgumentParser()
parser.add_argument(
  "mode", 
  choices=[VALID_ARGUMENTS.RUN_ONCE, VALID_ARGUMENTS.GUI, VALID_ARGUMENTS.CLEAN, VALID_ARGUMENTS.INIT_DB]
)
parser.add_argument(
  VALID_ARGUMENTS.NO_SOUND, 
  action="store_true", 
  help="Disable completion alert"
)

args = parser.parse_args()

arg = args.mode

match arg:
  case VALID_ARGUMENTS.RUN_ONCE:
    run_azb()
  case VALID_ARGUMENTS.GUI:
    run_gui()
  case VALID_ARGUMENTS.CLEAN:
    run_clean()
  case VALID_ARGUMENTS.INIT_DB:
    initialise_db()
  case _:
    raise ValueError(f"invalid argument: {arg}")

print("AZB End.")

if not args.no_sound:
  alert()

input()
