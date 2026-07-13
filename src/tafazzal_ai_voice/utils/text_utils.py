"""
Text utility functions.
"""

import re


def clean_text(text: str) -> str:
    """
    Remove extra spaces.
    """
    return re.sub(r"\s+", " ", text).strip()


def word_count(text: str) -> int:
    """
    Count words.
    """
    return len(clean_text(text).split())


def character_count(text: str) -> int:
    """
    Count characters.
    """
    return len(text)


def is_empty(text: str) -> bool:
    """
    Check whether text is empty.
    """
    return clean_text(text) == ""