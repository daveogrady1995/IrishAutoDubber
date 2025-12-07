"""
Video processing service
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import tempfile

from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment

from services.progress_observer import ProgressObserver, NoOpProgressObserver


class VideoService(ABC):
    """Abstract base class for video processing services"""

    @abstractmethod
    def load_video(self, video_path: Path) -> VideoFileClip:
        """Load a video file"""
        pass

    @abstractmethod
    def create_dubbed_video(
        self, video: VideoFileClip, audio_track: AudioSegment, output_path: Path
    ) -> Path:
        """Create final dubbed video by combining video with new audio"""
        pass

    @abstractmethod
    def get_video_duration(self, video: VideoFileClip) -> float:
        """Get video duration in seconds"""
        pass


class MoviePyVideoService(VideoService):
    """Video processing service using MoviePy"""

    def __init__(self, observer: Optional[ProgressObserver] = None):
        """
        Initialize MoviePy video service

        Args:
            observer: Progress observer for status updates
        """
        self.observer = observer or NoOpProgressObserver()

    def load_video(self, video_path: Path) -> VideoFileClip:
        """
        Load a video file using MoviePy

        Args:
            video_path: Path to video file

        Returns:
            VideoFileClip instance

        Raises:
            RuntimeError: If video cannot be loaded
        """
        try:
            self.observer.on_stage_start("Loading video")
            video = VideoFileClip(str(video_path))
            self.observer.on_stage_complete("Loading video")
            return video
        except Exception as e:
            error_msg = f"Failed to load video: {e}"
            self.observer.on_error(error_msg)
            raise RuntimeError(error_msg)

    def create_dubbed_video(
        self, video: VideoFileClip, audio_track: AudioSegment, output_path: Path
    ) -> Path:
        """
        Create final dubbed video by replacing audio track

        Args:
            video: Original video clip
            audio_track: New audio track (pydub AudioSegment)
            output_path: Path for output video file

        Returns:
            Path to created video file

        Raises:
            RuntimeError: If video creation fails
        """
        temp_dir = Path(tempfile.gettempdir())
        temp_audio_path = temp_dir / "dubbed_audio.wav"
        temp_audiofile = temp_dir / "temp_audio.m4a"

        try:
            self.observer.on_stage_start("Mixing audio and video")

            # Export audio track to temporary file
            audio_track.export(str(temp_audio_path), format="wav")

            # Create MoviePy audio clip
            new_audioclip = AudioFileClip(str(temp_audio_path))

            # Combine video with new audio
            final_video = video.with_audio(new_audioclip)

            # Write output video
            final_video.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac",
                threads=4,
                preset="fast",
                logger=None,  # Suppress MoviePy logging
                temp_audiofile=str(temp_audiofile),
                temp_audiofile_path=str(temp_dir),
            )

            self.observer.on_stage_complete("Mixing audio and video")

            # Cleanup temporary files
            self._cleanup_temp_files([temp_audio_path, temp_audiofile])

            return output_path

        except Exception as e:
            error_msg = f"Failed to create dubbed video: {e}"
            self.observer.on_error(error_msg)
            # Try to cleanup even on error
            self._cleanup_temp_files([temp_audio_path, temp_audiofile])
            raise RuntimeError(error_msg)

    def get_video_duration(self, video: VideoFileClip) -> float:
        """
        Get video duration in seconds

        Args:
            video: VideoFileClip instance

        Returns:
            Duration in seconds
        """
        return video.duration

    def _cleanup_temp_files(self, files: list[Path]):
        """Remove temporary files"""
        for file in files:
            try:
                if file.exists():
                    file.unlink()
            except Exception:
                pass  # Ignore cleanup errors
