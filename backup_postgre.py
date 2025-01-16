import os
from dotenv import load_dotenv
from datetime import datetime
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

# Create the backup directory if it doesn't exist
os.makedirs(BACKUP_PATH, exist_ok=True)

# Generate backup file name with timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
backup_file = os.path.join(BACKUP_PATH, f"{POSTGRES_DATABASE}_backup_{timestamp}.sql")

# Perform the backup
try:
    logging.info("Starting backup for database: %s", POSTGRES_DATABASE)
    print(f"Starting backup for database: {POSTGRES_DATABASE}")

    backup_command = [
        "pg_dump",
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

    subprocess.run(backup_command, check=True, env=env)
    logging.info("Backup completed successfully! File saved to: %s", backup_file)
    print(f"Backup completed successfully! File saved to: {backup_file}")

except subprocess.CalledProcessError as e:
    logging.error("Error during backup: %s", e)
    print(f"Error during backup: {e}")
except Exception as e:
    logging.error("Unexpected error: %s", e)
    print(f"Unexpected error: {e}")
