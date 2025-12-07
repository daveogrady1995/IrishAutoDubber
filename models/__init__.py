"""
Domain models for Irish Auto-Dubbing application
"""

from .voice_config import VoiceConfig
from .segment import Segment
from .dub_job import DubbingJob

__all__ = ["VoiceConfig", "Segment", "DubbingJob"]
