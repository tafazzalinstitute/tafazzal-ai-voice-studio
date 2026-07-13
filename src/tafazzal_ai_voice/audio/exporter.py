"""
Audio Exporter.
"""


class AudioExporter:
    """Export processed audio."""

    def export(self, file_path: str):
        return {
            "status": "exported",
            "file": file_path,
        }