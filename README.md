# AutoZipBackup (AZB)

A Python tool that checks source directories for changes and creates zip backups in destination directories.

## Getting Started

1. Install dependencies
   
   `pip install -r requirements.txt`

2. Configure settings
   
   Copy `azb_settings_example.json` to `azb_settings.json` and edit as needed

3. Initialise the database
   
   Run once to create the required tables in `azb.db`:
   `python azb.py init_db`

4. Configure directories
   
   Run the GUI to add source and destination directories:
   `python azb.py gui`

## Run Commands

Run the program using one of the following commands:

- `python azb.py run_once` - Performs a single backup run
- `python azb.py gui` - Launches the graphical user interface for managing source and destination directories
- `python azb.py clean` - Removes older zip backups from each destination directory, keeping the most recent N per directory as configured by `clean.keepRecentZipsPerDirectory` in `azb_settings.json`
- `python azb.py init_db` - Initialises the database tables