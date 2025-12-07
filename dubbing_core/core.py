"""
Centralized dubbing pipeline using service-oriented architecture.

This module provides a clean interface to the dubbing process while
delegating responsibilities to specialized services following SOLID principles.
"""

from pathlib import Path

from models import DubbingJob
from services import (
    AbairAudioService,
    MoviePyVideoService,
    SRTSubtitleService,
    ConsoleProgressObserver,
    DubbingOrchestrator,
)


def run_dubbing_process(video_path, eng_srt_path, gael_srt_path, output_filename):
    """
    Execute the entire dubbing pipeline.

    This function creates and coordinates all necessary services to convert
    a video with English subtitles to Irish-dubbed audio with synchronized subtitles.

    Args:
        video_path (str): Full path to input video file
        eng_srt_path (str): Full path to English SRT subtitle file
        gael_srt_path (str): Full path to Irish SRT subtitle file
        output_filename (str): Desired output filename (saved next to input video)

    Returns:
        str: Success message with output path, or error message prefixed with 'ERROR:'

    Architecture:
        This function follows the Dependency Inversion Principle by depending on
        service abstractions rather than concrete implementations. The orchestrator
        pattern coordinates the workflow while individual services handle their
        specific responsibilities (Single Responsibility Principle).
    """
    # Create dubbing job from input paths
    job = DubbingJob.from_paths(
        video_path, eng_srt_path, gael_srt_path, output_filename
    )

    # Initialize services
    observer = ConsoleProgressObserver()
    audio_service = AbairAudioService(job.current_folder, observer)
    video_service = MoviePyVideoService(observer)
    subtitle_service = SRTSubtitleService(observer)

    # Create orchestrator with dependency injection
    orchestrator = DubbingOrchestrator(
        audio_service=audio_service,
        video_service=video_service,
        subtitle_service=subtitle_service,
        observer=observer,
    )

    # Execute dubbing workflow
    return orchestrator.execute(job)
