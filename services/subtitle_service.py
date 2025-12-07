"""
Subtitle processing service
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from models.segment import Segment
from services.progress_observer import ProgressObserver, NoOpProgressObserver


class SubtitleService(ABC):
    """Abstract base class for subtitle processing services"""

    @abstractmethod
    def load_subtitles(self, eng_srt_path: Path, irish_srt_path: Path) -> List[Segment]:
        """Load and combine English and Irish subtitle files"""
        pass

    @abstractmethod
    def write_subtitles(
        self, output_path: Path, segments: List[Segment], language: str
    ):
        """Write subtitle segments to SRT file"""
        pass


class SRTSubtitleService(SubtitleService):
    """Subtitle service for SRT file format"""

    def __init__(self, observer: Optional[ProgressObserver] = None):
        """
        Initialize SRT subtitle service

        Args:
            observer: Progress observer for status updates
        """
        self.observer = observer or NoOpProgressObserver()

    def load_subtitles(self, eng_srt_path: Path, irish_srt_path: Path) -> List[Segment]:
        """
        Load and combine English and Irish subtitle files

        Args:
            eng_srt_path: Path to English SRT file
            irish_srt_path: Path to Irish SRT file

        Returns:
            List of Segment objects with combined timings and text

        Raises:
            RuntimeError: If files cannot be parsed or have mismatched segments
        """
        try:
            self.observer.on_stage_start("Parsing SRT files")

            eng_segments = self._parse_srt(eng_srt_path)
            irish_segments = self._parse_srt(irish_srt_path)

            if len(eng_segments) != len(irish_segments):
                raise RuntimeError(
                    f"SRT files have mismatched segment counts: "
                    f"English={len(eng_segments)}, Irish={len(irish_segments)}"
                )

            # Combine into Segment objects
            segments = []
            for i, (eng, irish) in enumerate(zip(eng_segments, irish_segments)):
                # Warn if timings don't match
                if eng["start"] != irish["start"] or eng["end"] != irish["end"]:
                    self.observer.on_progress(
                        i + 1,
                        len(eng_segments),
                        "Parsing",
                        f"Warning: Timing mismatch at segment {i + 1}",
                    )

                segment = Segment(
                    start=eng["start"],
                    end=eng["end"],
                    english_text=eng["text"],
                    irish_text=irish["text"],
                    index=i + 1,
                )
                segments.append(segment)

            self.observer.on_stage_complete("Parsing SRT files")
            return segments

        except Exception as e:
            error_msg = f"Failed to load subtitles: {e}"
            self.observer.on_error(error_msg)
            raise RuntimeError(error_msg)

    def write_subtitles(
        self, output_path: Path, segments: List[Segment], language: str
    ):
        """
        Write subtitle segments to SRT file

        Args:
            output_path: Path for output SRT file
            segments: List of Segment objects to write
            language: Language to write ('english' or 'irish')

        Raises:
            RuntimeError: If file cannot be written
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for i, segment in enumerate(segments, start=1):
                    # Get text based on language
                    if language.lower() == "english":
                        text = segment.get_clean_english_text()
                    else:  # irish
                        text = segment.irish_text

                    # Write SRT entry
                    f.write(f"{i}\n")
                    f.write(
                        f"{self._format_srt_time(segment.start)} --> "
                        f"{self._format_srt_time(segment.end)}\n"
                    )
                    f.write(f"{text}\n\n")

        except Exception as e:
            error_msg = f"Failed to write subtitles: {e}"
            self.observer.on_error(error_msg)
            raise RuntimeError(error_msg)

    def _parse_srt(self, file_path: Path) -> List[dict]:
        """
        Parse an SRT file into raw segments

        Returns:
            List of dicts with 'start', 'end', 'text' keys
        """
        segments = []

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Look for segment index (number)
            if line.isdigit():
                # Next line should be timing
                if i + 1 < len(lines):
                    time_line = lines[i + 1].strip()
                    if " --> " in time_line:
                        start_str, end_str = time_line.split(" --> ")
                        start = self._parse_time(start_str)
                        end = self._parse_time(end_str)

                        # Collect text lines
                        text_lines = []
                        i += 2
                        while i < len(lines) and lines[i].strip():
                            text_lines.append(lines[i].strip())
                            i += 1

                        text = " ".join(text_lines)
                        segments.append({"start": start, "end": end, "text": text})
                        continue

            i += 1

        return segments

    def _parse_time(self, time_str: str) -> float:
        """
        Parse SRT timestamp to seconds

        Format: HH:MM:SS,mmm
        """
        hours, minutes, secs_millis = time_str.split(":")
        secs, millis = secs_millis.split(",")

        return (
            float(hours) * 3600
            + float(minutes) * 60
            + float(secs)
            + float(millis) / 1000
        )

    def _format_srt_time(self, seconds: float) -> str:
        """
        Format seconds to SRT timestamp

        Format: HH:MM:SS,mmm
        """
        import datetime

        td = datetime.timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        millis = int((seconds - total_seconds) * 1000)

        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
