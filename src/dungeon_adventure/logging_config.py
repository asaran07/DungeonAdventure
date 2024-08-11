import logging.config
import os
from datetime import datetime

# Get the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to get to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Create a logs directory if it doesn't exist
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Create a new log file for each run
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOGS_DIR, f"game_{current_time}.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
        },
        "simple": {"format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "simple",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "DEBUG",
            "formatter": "detailed",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE,
            "mode": "a",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "dungeon_adventure": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "dungeon_adventure.combat": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "pygame": {"handlers": ["file"], "level": "WARNING", "propagate": False},
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
