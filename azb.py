from sys import argv
from time import sleep

from modules.azb_engine import run_azb

for i in range(len(argv)):
  print(f"Arg #{i}: {argv[i]}")

RUN_ONCE_ARG = "run_once"
RUN_DAILY_ARG = "run_daily"
RUN_WHEN_DIRS_AVAILABLE_ARG = "run_when_dirs_available"
CLI_ARG = "cli"
GUI_ARG = "gui"

VALID_ARGUMENTS = [
  RUN_ONCE_ARG,
  RUN_DAILY_ARG,
  RUN_WHEN_DIRS_AVAILABLE_ARG
]

if len(argv) != 2:
  raise ValueError("bad input. usage: python azb.py <valid argument>")

# Arg #0: azb.py
arg = argv[1]
if arg not in VALID_ARGUMENTS:
  raise ValueError(f"invalid argument: {arg}")

match arg:
  case "run_once":
    run_azb()
  case "run_daily":
    pass
  case "run_when_dirs_available":
    pass

print("AZB End.")
input()
