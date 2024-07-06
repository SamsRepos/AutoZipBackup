from sys import argv
from time import sleep

from modules.azb_engine import run_azb

for i in range(len(argv)):
  print(f"Arg #{i}: {argv[i]}")

class VALID_ARGUMENTS:
  RUN_ONCE                = "run_once"
  RUN_DAILY               = "run_daily"
  RUN_WHEN_DIRS_AVAILABLE = "run_when_dirs_available"
  CLI                     = "cli"
  GUI                     = "gui"

if len(argv) != 2:
  raise ValueError("bad input. usage: python azb.py <valid argument>")

# Arg #0: azb.py
arg = argv[1]

match arg:
  case VALID_ARGUMENTS.RUN_ONCE:
    run_azb()
  case VALID_ARGUMENTS.RUN_DAILY:
    pass
  case VALID_ARGUMENTS.RUN_WHEN_DIRS_AVAILABLE:
    pass
  case VALID_ARGUMENTS.CLI:
    pass
  case VALID_ARGUMENTS.GUI:
    pass
  case _:
    raise ValueError(f"invalid argument: {arg}")

print("AZB End.")
input()
