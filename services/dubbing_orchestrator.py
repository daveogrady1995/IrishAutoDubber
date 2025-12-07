"""
Dubbing orchestrator - coordinates all services to perform dubbing
"""

import random
import time
from pathlib import Path
from typing import List, Optional
from pydub import AudioSegment

from models import DubbingJob, Segment, VoiceConfig
from services import (
    AudioService,
    VideoService,
    SubtitleService,
    ProgressObserver,
    ConsoleProgressObserver,
)


class DubbingOrchestrator:
    """
    Orchestrates the entire dubbing workflow using service layer

    This class follows the Single Responsibility Principle by delegating
    specific tasks to dedicated services while coordinating the overall flow.
    """

    # Configuration constants
    LONG_TEXT_THRESHOLD = 60  # Characters
    CHARS_PER_SEC_READING_SPEED = 14  # Average reading speed
    SKIP_THRESHOLD_SEC = 2.5
    SEGMENT_DELAY_SEC = 5  # Delay between segments

    # Available voices
    VOICE_POOL = [
        VoiceConfig(dialect="Kerry", gender="Female"),
        VoiceConfig(dialect="Kerry", gender="Male"),
    ]

    def __init__(
        self,
        audio_service: AudioService,
        video_service: VideoService,
        subtitle_service: SubtitleService,
        observer: Optional[ProgressObserver] = None,
    ):
        """
        Initialize dubbing orchestrator

        Args:
            audio_service: Service for audio generation
            video_service: Service for video processing
            subtitle_service: Service for subtitle handling
            observer: Progress observer for status updates
        """
        self.audio_service = audio_service
        self.video_service = video_service
        self.subtitle_service = subtitle_service
        self.observer = observer or ConsoleProgressObserver()

    def execute(self, job: DubbingJob) -> str:
        """
        Execute complete dubbing workflow

        Args:
            job: DubbingJob containing all necessary parameters

        Returns:
            Success message with output path, or error message prefixed with 'ERROR:'
        """
        # Validate job
        error = job.validate()
        if error:
            return f"ERROR: {error}"

        try:
            # Step 1: Load subtitles
            job.segments = self.subtitle_service.load_subtitles(
                job.eng_srt_path, job.gael_srt_path
            )

            # Step 2: Load video
            video = self.video_service.load_video(job.video_path)
            video_duration = self.video_service.get_video_duration(video)

            # Step 3: Setup audio service
            self.audio_service.setup()

            try:
                # Step 4: Generate dubbed audio track
                dub_track, processed_segments = self._generate_dub_track(
                    job.segments, video_duration, job.current_folder
                )

                # Step 5: Create final video
                self.video_service.create_dubbed_video(
                    video, dub_track, job.output_path
                )

                # Step 6: Write subtitle files
                self._write_subtitle_files(job, processed_segments)

                # Success
                self.observer.on_complete(str(job.output_path))
                return f"Success! Output video saved as: {job.output_path}"

            finally:
                # Always cleanup audio service
                self.audio_service.cleanup()

        except Exception as e:
            error_msg = f"ERROR: Dubbing process failed: {e}"
            self.observer.on_error(str(e))
            return error_msg

    def _generate_dub_track(
        self, segments: List[Segment], video_duration: float, output_dir: Path
    ) -> tuple[AudioSegment, List[Segment]]:
        """
        Generate complete dubbed audio track

        Returns:
            Tuple of (audio_track, processed_segments_with_timing)
        """
        self.observer.on_stage_start("Dubbing audio")

        dub_track = AudioSegment.silent(duration=0)
        processed_segments = []
        current_time_ms = 0
        previous_voice = None

        for i, segment in enumerate(segments):
            # Update progress
            self.observer.on_progress(
                i + 1,
                len(segments),
                "Dubbing",
                f"Segment {i + 1}/{len(segments)}",
            )

            # Skip empty segments
            if segment.is_empty():
                continue

            # Select voice
            voice = self._select_voice(segment, previous_voice)

            # Calculate smart timing
            allowed_end_sec = self._calculate_smart_timing(
                segment, i, segments, video_duration
            )

            # Add sync silence
            gap_ms = segment.start_ms - current_time_ms
            if gap_ms > 0:
                dub_track += AudioSegment.silent(duration=gap_ms)
                current_time_ms += gap_ms
            elif gap_ms < -(self.SKIP_THRESHOLD_SEC * 1000):
                self.observer.on_progress(
                    i + 1, len(segments), "Dubbing", f"Skipping segment {i + 1} (lag)"
                )
                continue

            # Generate audio
            audio_path = self.audio_service.generate_audio(
                segment.irish_text, voice, output_dir
            )

            if audio_path:
                # Add audio to track
                voice_audio = AudioSegment.from_file(str(audio_path))
                dub_track += voice_audio
                current_time_ms += len(voice_audio)

                # Record processed segment
                processed_segment = Segment(
                    start=segment.start,
                    end=allowed_end_sec,
                    english_text=segment.get_clean_english_text(),
                    irish_text=segment.irish_text,
                    index=len(processed_segments) + 1,
                )
                processed_segments.append(processed_segment)

                previous_voice = voice

                # Delay between segments
                time.sleep(self.SEGMENT_DELAY_SEC)
            else:
                # Fallback to silence
                fallback_duration = segment.duration_ms
                if gap_ms > 0:
                    dub_track += AudioSegment.silent(duration=fallback_duration)
                    current_time_ms += fallback_duration

        self.observer.on_stage_complete("Dubbing audio")
        return dub_track, processed_segments

    def _select_voice(
        self, segment: Segment, previous_voice: Optional[VoiceConfig]
    ) -> VoiceConfig:
        """
        Select appropriate voice for segment

        Uses gender marker (#) to determine male/female voice
        """
        if segment.has_male_marker():
            # Male voice
            male_voices = [v for v in self.VOICE_POOL if v.gender == "Male"]
            return random.choice(male_voices)
        else:
            # Female voice
            female_voices = [v for v in self.VOICE_POOL if v.gender == "Female"]
            return random.choice(female_voices)

    def _calculate_smart_timing(
        self,
        segment: Segment,
        index: int,
        all_segments: List[Segment],
        video_duration: float,
    ) -> float:
        """
        Calculate appropriate end time for subtitle based on text length

        Returns:
            Adjusted end time in seconds
        """
        char_count = len(segment.irish_text)
        min_reading_time_sec = char_count / self.CHARS_PER_SEC_READING_SPEED

        # Add extra time for long text
        if char_count > self.LONG_TEXT_THRESHOLD:
            min_reading_time_sec += 1.5

        # Use larger of original duration or calculated reading time
        final_duration = max(segment.duration, min_reading_time_sec)

        # Look ahead to avoid overlap with next segment
        next_start = (
            all_segments[index + 1].start
            if (index + 1 < len(all_segments))
            else video_duration
        )

        # Extend into silence gap if needed, but leave small buffer
        allowed_end = min(segment.start + final_duration, next_start - 0.1)

        return allowed_end

    def _write_subtitle_files(self, job: DubbingJob, segments: List[Segment]):
        """Write both English and Irish subtitle files"""
        self.observer.on_stage_start("Writing subtitles")

        # Write English subtitles
        self.subtitle_service.write_subtitles(
            job.output_srt_english, segments, "english"
        )

        # Write Irish subtitles
        self.subtitle_service.write_subtitles(job.output_srt_irish, segments, "irish")

        self.observer.on_stage_complete("Writing subtitles")
