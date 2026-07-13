"""
Professional logging system for Tafazzal AI Voice Studio.
"""

from __future__ import annotations

import logging
from pathlib import Path


LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str = "tafazzal_ai_voice",
    level: int = logging.INFO,
    log_directory: str = "logs",
) -> logging.Logger:
    """
    Create and configure application logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    Path(log_directory).mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        LOG_FORMAT,
        DATE_FORMAT,
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        Path(log_directory) / "application.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()