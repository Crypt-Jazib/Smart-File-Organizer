import logging
from pathlib import Path

LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "organizer.log"


logger = logging.getLogger("SmartFileOrganizer")

logger.setLevel(logging.INFO)

logger.propagate = False

if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)