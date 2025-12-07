"""
Subtitle segment model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Segment:
    """Represents a single subtitle segment with timing and text"""

    start: float  # Start time in seconds
    end: float  # End time in seconds
    english_text: str
    irish_text: str
    index: Optional[int] = None

    @property
    def duration(self) -> float:
        """Get segment duration in seconds"""
        return self.end - self.start

    @property
    def start_ms(self) -> int:
        """Get start time in milliseconds"""
        return int(self.start * 1000)

    @property
    def end_ms(self) -> int:
        """Get end time in milliseconds"""
        return int(self.end * 1000)

    @property
    def duration_ms(self) -> int:
        """Get duration in milliseconds"""
        return int(self.duration * 1000)

    def has_male_marker(self) -> bool:
        """Check if segment is marked for male voice (ends with #)"""
        return self.english_text.endswith("#")

    def get_clean_english_text(self) -> str:
        """Get English text with voice markers removed"""
        return self.english_text.rstrip("#")

    def is_empty(self) -> bool:
        """Check if segment has no Irish text"""
        return not self.irish_text or not self.irish_text.strip()
