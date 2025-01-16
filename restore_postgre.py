import os
from dotenv import load_dotenv
import subprocess
import logging

# Load environment variables from credentials.env
load_dotenv("credentials.env")

# Environment variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
BACKUP_PATH = os.getenv("BACKUP_PATH")

# Ensure BACKUP_PATH is set
if not BACKUP_PATH:
    raise ValueError("BACKUP_PATH is not defined in the credentials.env file.")

# Path for the log file
LOG_DIR = os.path.join("D:\\takemytickets4\\backup_restore\\logs")  # Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "backup.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# List available backup files
try:
    logging.info("Checking for backup files in directory: %s", BACKUP_PATH)
    print(f"Backup directory: {BACKUP_PATH}")

    # List SQL files in the backup directory
    backup_files = [f for f in os.listdir(BACKUP_PATH) if f.endswith(".sql")]

    if not backup_files:
        logging.warning("No backup files found in the backup directory.")
        print("No backup files found in the backup directory.")
        exit()

    print("Available backup files:")
    for i, file in enumerate(backup_files, 1):
        print(f"{i}. {file}")

    # Ask the user to choose a file
    file_index = int(input("Enter the number of the file you want to restore: ")) - 1
    if file_index < 0 or file_index >= len(backup_files):
        logging.error("Invalid selection by the user.")
        print("Invalid selection. Exiting.")
        exit()

    # Selected backup file
    backup_file = os.path.join(BACKUP_PATH, backup_files[file_index])
    logging.info("Selected backup file: %s", backup_file)
    print(f"Selected backup file: {backup_file}")

    # Perform the restore
    logging.info("Starting restore for database: %s", POSTGRES_DATABASE)
    print(f"Starting restore for database: {POSTGRES_DATABASE}")

    restore_command = [
        "psql",
        f"--host={POSTGRES_HOST}",
        f"--port={POSTGRES_PORT}",
        f"--username={POSTGRES_USER}",
        f"--dbname={POSTGRES_DATABASE}",
        "--no-password",
        f"--file={backup_file}"
    ]

    # Set the environment variable for the password
    env = os.environ.copy()
    env["PGPASSWORD"] = POSTGRES_PASSWORD

    subprocess.run(restore_command, check=True, env=env)
    logging.info("Restore completed successfully from file: %s", backup_file)
    print(f"Restore completed successfully from file: {backup_file}")

except subprocess.CalledProcessError as e:
    logging.error("Error during restore: %s", e)
    print(f"Error during restore: {e}")
except Exception as e:
    logging.error("Unexpected error: %s", e)
    print(f"Unexpected error: {e}")
