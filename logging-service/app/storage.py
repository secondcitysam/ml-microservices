
import json
import os
from pathlib import Path
from threading import Lock


# Locate the logging-service directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the log storage directory
LOG_DIR = BASE_DIR / "logs"

# Define the log file
LOG_FILE = LOG_DIR / "application.jsonl"

# Prevent simultaneous writes from interfering
FILE_LOCK = Lock()


def initialize_storage():
    """
    Create the log directory and file if they do not exist.
    """

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    LOG_FILE.touch(
        exist_ok=True
    )


def save_log(log_entry):
    """
    Append one log record to the JSON Lines file.
    """

    initialize_storage()

    with FILE_LOCK:

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    log_entry,
                    allow_nan=False
                ) + "\n"
            )


def get_logs(limit=100):
    """
    Retrieve the most recent log records.
    """

    initialize_storage()

    logs = []

    with FILE_LOCK:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                if line.strip():

                    logs.append(
                        json.loads(line)
                    )

    # Return the most recent records
    return logs[-limit:]
