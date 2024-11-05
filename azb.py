from sys import argv
from time import sleep

from modules.azb_engine import run_azb
from modules.azb_gui import run_gui

for i in range(len(argv)):
  print(f"Arg #{i}: {argv[i]}")

class VALID_ARGUMENTS:
  RUN_ONCE                = "run_once"
  CLI                     = "cli"
  GUI                     = "gui"

if len(argv) != 2:
  raise ValueError("bad input. usage: python azb.py <valid argument>")

# Arg #0: azb.py
arg = argv[1]

match arg:
  case VALID_ARGUMENTS.RUN_ONCE:
    run_azb()
  case VALID_ARGUMENTS.CLI:
    pass
  case VALID_ARGUMENTS.GUI:
    run_gui()
  case _:
    raise ValueError(f"invalid argument: {arg}")

print("AZB End.")
input()
