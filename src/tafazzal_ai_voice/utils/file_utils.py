"""
File utility functions.
"""

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """
    Create directory if it does not exist.
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def file_exists(path: str | Path) -> bool:
    """
    Check whether a file exists.
    """
    return Path(path).exists()


def write_text(path: str | Path, text: str) -> None:
    """
    Write text to file.
    """
    Path(path).write_text(text, encoding="utf-8")


def read_text(path: str | Path) -> str:
    """
    Read text from file.
    """
    return Path(path).read_text(encoding="utf-8")