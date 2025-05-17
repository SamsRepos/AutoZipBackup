AutoZipBackup (AZB)
==================

A Python tool that checks source directories for changes and creates zip backups in destination directories.

Usage
-----

Run the program using one of the following commands:

- `python azb.py run_once` - Performs a single backup operation
- `python azb.py gui` - Launches the graphical user interface for managing source and destination directories

Configuration
------------

The program uses a SQLite database (`azb.db`) to store configuration settings. You can configure source and destination directories through the GUI interface.
