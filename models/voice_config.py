"""
Voice configuration model
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class VoiceConfig:
    """Represents voice settings for TTS generation"""

    dialect: Literal["Kerry", "Connemara", "Galway"]
    gender: Literal["Male", "Female"]

    def __eq__(self, other):
        """Check if two voice configs are identical"""
        if not isinstance(other, VoiceConfig):
            return False
        return self.dialect == other.dialect and self.gender == other.gender

    def __hash__(self):
        """Allow VoiceConfig to be used as dictionary key"""
        return hash((self.dialect, self.gender))

    def needs_speed_adjustment(self) -> bool:
        """Check if this voice needs speed adjustment (Connemara Female)"""
        return self.dialect == "Connemara" and self.gender == "Female"

    def speed_multiplier(self) -> float:
        """Get speed multiplier for this voice"""
        return 1.4 if self.needs_speed_adjustment() else 1.0
