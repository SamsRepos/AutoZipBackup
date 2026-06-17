AutoZipBackup (AZB)
==================

A Python tool that checks source directories for changes and creates zip backups in destination directories.

Usage
-----

Run the program using one of the following commands:

- `python azb.py run_once` - Performs a single backup operation
- `python azb.py gui` - Launches the graphical user interface for managing source and destination directories
- `python azb.py clean` - Removes older zip backups from each destination directory, keeping the most recent N per directory as configured by clean.keepRecentZipsPerDirectory in azb_settings.json

Configuration
------------

The program uses a SQLite database (`azb.db`) to store configuration settings. You can configure source and destination directories through the GUI interface.
