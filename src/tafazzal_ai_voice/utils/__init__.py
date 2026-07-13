"""
Utility package.
"""

from .file_utils import (
    ensure_directory,
    file_exists,
    read_text,
    write_text,
)

from .text_utils import (
    clean_text,
    word_count,
    character_count,
    is_empty,
)

__all__ = [
    "ensure_directory",
    "file_exists",
    "read_text",
    "write_text",
    "clean_text",
    "word_count",
    "character_count",
    "is_empty",
]