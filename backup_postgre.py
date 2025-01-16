import os
from dotenv import load_dotenv
from datetime import datetime
import subprocess

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

# Create the backup directory if it doesn't exist
os.makedirs(BACKUP_PATH, exist_ok=True)

# Generate backup file name with timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
backup_file = os.path.join(BACKUP_PATH, f"{POSTGRES_DATABASE}_backup_{timestamp}.sql")

# Perform the backup
try:
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
    print(f"Backup completed successfully! File saved to: {backup_file}")

except subprocess.CalledProcessError as e:
    print(f"Error during backup: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
