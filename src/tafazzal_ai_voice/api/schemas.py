"""
API Schemas.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class VoiceRequest:
    """Voice generation request."""

    text: str


@dataclass(slots=True)
class VoiceResponse:
    """Voice generation response."""

    status: str
    message: str