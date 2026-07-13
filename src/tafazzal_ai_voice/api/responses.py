"""
API Responses.
"""


def success(message: str):
    """Success response."""

    return {
        "status": "success",
        "message": message,
    }


def error(message: str):
    """Error response."""

    return {
        "status": "error",
        "message": message,
    }