# main.py

import argparse
import subprocess
import os
import logging
import config  # Import the config file

# Configure logging
logging.basicConfig(level=config.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s', filename=config.LOG_FILE)

def run_script(script_path, description):
    """Runs a Python script and prints its output."""
    logging.info(f"Running {description}...")
    try:
        subprocess.run(["python", script_path], check=True)
        logging.info(f"{description} completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running {description}: {e}")
    except FileNotFoundError:
        logging.error(f"Error: {script_path} not found.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Run CVE project scripts in order.')
    parser.add_argument('--all', action='store_true', help='Run all scripts in order.')
    parser.add_argument('--setupdb', action='store_true', help='Setup the database.')
    parser.add_argument('--fetch', action='store_true', help='Fetch and store CVE data.')
    parser.add_argument('--sync', action='store_true', help='Run full sync of CVE data.')
    parser.add_argument('--run', action='store_true', help='Run the Flask application.')
    parser.add_argument('--test', action='store_true', help='Run the unit tests.')

    args = parser.parse_args()

    if args.all:
        run_script("database.py", "Database setup")
        run_script("fetch_CVE_data.py", "CVE data fetching")
        run_script("full_sync.py", "Full CVE data sync")
        run_script("api_fetch.py", "API fetch script")
        run_script("app2.py", "Flask application")
        run_script(os.path.join("tests", "unit_tests.py"), "Unit tests")
    else:
        if args.setupdb:
            run_script("database.py", "Database setup")
        if args.fetch:
            run_script("fetch_CVE_data.py", "CVE data fetching")
        if args.sync:
            run_script("full_sync.py", "Full CVE data sync")
        if args.run:
            run_script("app2.py", "Flask application")
        if args.test:
            run_script(os.path.join("tests", "unit_tests.py"), "Unit tests")

if __name__ == '__main__':
    main()