"""
Unit tests for service layer
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path
from pydub import AudioSegment

from models import VoiceConfig, Segment, DubbingJob
from services import (
    ProgressObserver,
    ConsoleProgressObserver,
    NoOpProgressObserver,
)


class TestProgressObserver(unittest.TestCase):
    """Test ProgressObserver implementations"""

    def test_noop_observer_does_nothing(self):
        """Test NoOpProgressObserver doesn't raise errors"""
        observer = NoOpProgressObserver()

        # Should not raise any exceptions
        observer.on_progress(1, 10, "Test", "message")
        observer.on_stage_start("Test Stage")
        observer.on_stage_complete("Test Stage")
        observer.on_error("Test error")
        observer.on_complete("/path/to/output")

    def test_console_observer_prints(self):
        """Test ConsoleProgressObserver prints messages"""
        observer = ConsoleProgressObserver()

        with patch("builtins.print") as mock_print:
            observer.on_stage_start("Testing")
            mock_print.assert_called_with("\nTesting...")

        with patch("builtins.print") as mock_print:
            observer.on_stage_complete("Testing")
            mock_print.assert_called_with("✓ Testing complete")

        with patch("builtins.print") as mock_print:
            observer.on_error("Test error")
            mock_print.assert_called_with("\n✗ Error: Test error")

        with patch("builtins.print") as mock_print:
            observer.on_complete("/output/path")
            mock_print.assert_called_with("\n✓ DONE! Output: /output/path")


class TestSubtitleService(unittest.TestCase):
    """Test SubtitleService"""

    def test_parse_srt_time(self):
        """Test SRT timestamp parsing"""
        from services.subtitle_service import SRTSubtitleService

        service = SRTSubtitleService()

        # Test: 00:01:23,456 = 83.456 seconds
        result = service._parse_time("00:01:23,456")
        self.assertAlmostEqual(result, 83.456, places=3)

        # Test: 01:00:00,000 = 3600 seconds
        result = service._parse_time("01:00:00,000")
        self.assertEqual(result, 3600.0)

    def test_format_srt_time(self):
        """Test SRT timestamp formatting"""
        from services.subtitle_service import SRTSubtitleService

        service = SRTSubtitleService()

        # Test: 83.456 seconds = 00:01:23,456
        result = service._format_srt_time(83.456)
        self.assertEqual(result, "00:01:23,456")

        # Test: 3600 seconds = 01:00:00,000
        result = service._format_srt_time(3600.0)
        self.assertEqual(result, "01:00:00,000")


class TestDubbingOrchestrator(unittest.TestCase):
    """Test DubbingOrchestrator"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_audio_service = Mock()
        self.mock_video_service = Mock()
        self.mock_subtitle_service = Mock()
        self.mock_observer = Mock(spec=ProgressObserver)

    def test_voice_selection_male_marker(self):
        """Test voice selection with male marker"""
        from services.dubbing_orchestrator import DubbingOrchestrator

        orchestrator = DubbingOrchestrator(
            self.mock_audio_service,
            self.mock_video_service,
            self.mock_subtitle_service,
            self.mock_observer,
        )

        # Segment with male marker (#)
        segment = Segment(
            start=1.0, end=2.0, english_text="Male voice#", irish_text="Guth fir"
        )

        voice = orchestrator._select_voice(segment, None)
        self.assertEqual(voice.gender, "Male")

    def test_voice_selection_female_default(self):
        """Test voice selection defaults to female"""
        from services.dubbing_orchestrator import DubbingOrchestrator

        orchestrator = DubbingOrchestrator(
            self.mock_audio_service,
            self.mock_video_service,
            self.mock_subtitle_service,
            self.mock_observer,
        )

        # Segment without male marker
        segment = Segment(
            start=1.0, end=2.0, english_text="Female voice", irish_text="Guth mná"
        )

        voice = orchestrator._select_voice(segment, None)
        self.assertEqual(voice.gender, "Female")

    def test_smart_timing_calculation(self):
        """Test smart timing calculation"""
        from services.dubbing_orchestrator import DubbingOrchestrator

        orchestrator = DubbingOrchestrator(
            self.mock_audio_service,
            self.mock_video_service,
            self.mock_subtitle_service,
            self.mock_observer,
        )

        # Short text segment
        segment = Segment(start=1.0, end=2.0, english_text="Hi", irish_text="Dia duit")

        segments = [
            segment,
            Segment(start=5.0, end=6.0, english_text="Next", irish_text="Ar aghaidh"),
        ]

        # Calculate timing for first segment
        allowed_end = orchestrator._calculate_smart_timing(segment, 0, segments, 100.0)

        # Should not extend past next segment
        self.assertLess(allowed_end, 5.0)

    def test_smart_timing_with_long_text(self):
        """Test smart timing adds extra time for long text"""
        from services.dubbing_orchestrator import DubbingOrchestrator

        orchestrator = DubbingOrchestrator(
            self.mock_audio_service,
            self.mock_video_service,
            self.mock_subtitle_service,
            self.mock_observer,
        )

        # Long text (>60 chars)
        long_irish_text = "A" * 70  # 70 characters
        segment = Segment(
            start=1.0, end=2.0, english_text="Long text", irish_text=long_irish_text
        )

        segments = [segment]

        allowed_end = orchestrator._calculate_smart_timing(segment, 0, segments, 100.0)

        # Should extend beyond original end time for long text
        self.assertGreater(allowed_end, segment.end)


class MockAudioService:
    """Mock audio service for testing"""

    def __init__(self):
        self.setup_called = False
        self.cleanup_called = False
        self.generate_calls = []

    def setup(self):
        self.setup_called = True

    def cleanup(self):
        self.cleanup_called = True

    def generate_audio(self, text, voice, output_dir):
        self.generate_calls.append((text, voice, output_dir))
        return None  # Return None to simulate failure


class TestServiceLifecycle(unittest.TestCase):
    """Test service lifecycle management"""

    def test_orchestrator_calls_setup_and_cleanup(self):
        """Test orchestrator properly manages service lifecycle"""
        from services.dubbing_orchestrator import DubbingOrchestrator

        mock_audio = MockAudioService()
        mock_video = Mock()
        mock_subtitle = Mock()
        mock_observer = Mock()

        # Mock subtitle service to return empty segments
        mock_subtitle.load_subtitles.return_value = []

        # Mock video service
        mock_video.load_video.return_value = Mock(duration=10.0)
        mock_video.get_video_duration.return_value = 10.0

        orchestrator = DubbingOrchestrator(
            mock_audio, mock_video, mock_subtitle, mock_observer
        )

        # Create a valid job
        job = DubbingJob(
            video_path=Path(__file__),  # Use this file as it exists
            eng_srt_path=Path(__file__),
            gael_srt_path=Path(__file__),
            output_filename="test.mp4",
        )

        # Execute (will fail due to missing files, but that's ok for lifecycle test)
        try:
            orchestrator.execute(job)
        except:
            pass

        # Verify setup and cleanup were called
        self.assertTrue(mock_audio.setup_called)
        self.assertTrue(mock_audio.cleanup_called)


if __name__ == "__main__":
    unittest.main()
