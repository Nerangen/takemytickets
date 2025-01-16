import os
from dotenv import load_dotenv
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

# List available backup files
print(f"Backup directory: {BACKUP_PATH}")
backup_files = [f for f in os.listdir(BACKUP_PATH) if f.endswith(".sql")]

if not backup_files:
    print("No backup files found in the backup directory.")
    exit()

print("Available backup files:")
for i, file in enumerate(backup_files, 1):
    print(f"{i}. {file}")

# Ask the user to choose a file
file_index = int(input("Enter the number of the file you want to restore: ")) - 1
if file_index < 0 or file_index >= len(backup_files):
    print("Invalid selection. Exiting.")
    exit()

backup_file = os.path.join(BACKUP_PATH, backup_files[file_index])
print(f"Selected backup file: {backup_file}")

# Perform the restore
try:
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
    print(f"Restore completed successfully from file: {backup_file}")

except subprocess.CalledProcessError as e:
    print(f"Error during restore: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
