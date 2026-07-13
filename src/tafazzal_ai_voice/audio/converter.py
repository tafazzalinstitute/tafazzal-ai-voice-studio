"""
Audio Converter.
"""


class AudioConverter:
    """Convert audio."""

    def convert(self, input_file: str, output_format: str):
        return {
            "input": input_file,
            "format": output_format,
        }