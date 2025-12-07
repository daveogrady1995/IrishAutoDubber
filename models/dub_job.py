"""
Dubbing job model
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from .segment import Segment


@dataclass
class DubbingJob:
    """Represents a complete dubbing job with all necessary parameters"""

    video_path: Path
    eng_srt_path: Path
    gael_srt_path: Path
    output_filename: str
    segments: List[Segment] = field(default_factory=list)

    @property
    def current_folder(self) -> Path:
        """Get the folder containing the video file"""
        return self.video_path.parent

    @property
    def output_path(self) -> Path:
        """Get the full output path"""
        return self.current_folder / self.output_filename

    @property
    def output_srt_english(self) -> Path:
        """Get the output English subtitle path"""
        return self.current_folder / "subtitles_english.srt"

    @property
    def output_srt_irish(self) -> Path:
        """Get the output Irish subtitle path"""
        return self.current_folder / "subtitles_irish.srt"

    def validate(self) -> Optional[str]:
        """
        Validate the dubbing job inputs

        Returns:
            Error message if validation fails, None if valid
        """
        if not self.video_path.exists():
            return f"Video file not found: {self.video_path}"

        if not self.eng_srt_path.exists():
            return f"English SRT file not found: {self.eng_srt_path}"

        if not self.gael_srt_path.exists():
            return f"Irish SRT file not found: {self.gael_srt_path}"

        if not self.output_filename:
            return "Output filename cannot be empty"

        return None

    @classmethod
    def from_paths(
        cls,
        video_path: str,
        eng_srt_path: str,
        gael_srt_path: str,
        output_filename: str,
    ):
        """Create a DubbingJob from string paths"""
        return cls(
            video_path=Path(video_path),
            eng_srt_path=Path(eng_srt_path),
            gael_srt_path=Path(gael_srt_path),
            output_filename=output_filename,
        )
