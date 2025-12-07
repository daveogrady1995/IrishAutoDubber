"""
Unit tests for domain models
"""

import unittest
from pathlib import Path
from models import VoiceConfig, Segment, DubbingJob


class TestVoiceConfig(unittest.TestCase):
    """Test VoiceConfig domain model"""

    def test_voice_config_creation(self):
        """Test creating a VoiceConfig"""
        voice = VoiceConfig(dialect="Kerry", gender="Female")
        self.assertEqual(voice.dialect, "Kerry")
        self.assertEqual(voice.gender, "Female")

    def test_voice_config_equality(self):
        """Test voice config equality comparison"""
        voice1 = VoiceConfig(dialect="Kerry", gender="Female")
        voice2 = VoiceConfig(dialect="Kerry", gender="Female")
        voice3 = VoiceConfig(dialect="Kerry", gender="Male")

        self.assertEqual(voice1, voice2)
        self.assertNotEqual(voice1, voice3)

    def test_voice_config_hash(self):
        """Test voice config can be used as dict key"""
        voice1 = VoiceConfig(dialect="Kerry", gender="Female")
        voice2 = VoiceConfig(dialect="Kerry", gender="Female")

        voice_dict = {voice1: "test"}
        self.assertIn(voice2, voice_dict)

    def test_connemara_female_needs_speed_adjustment(self):
        """Test Connemara Female voice needs speed adjustment"""
        voice = VoiceConfig(dialect="Connemara", gender="Female")
        self.assertTrue(voice.needs_speed_adjustment())
        self.assertEqual(voice.speed_multiplier(), 1.4)

    def test_other_voices_no_speed_adjustment(self):
        """Test other voices don't need speed adjustment"""
        voices = [
            VoiceConfig(dialect="Kerry", gender="Female"),
            VoiceConfig(dialect="Kerry", gender="Male"),
            VoiceConfig(dialect="Connemara", gender="Male"),
        ]

        for voice in voices:
            self.assertFalse(voice.needs_speed_adjustment())
            self.assertEqual(voice.speed_multiplier(), 1.0)


class TestSegment(unittest.TestCase):
    """Test Segment domain model"""

    def test_segment_creation(self):
        """Test creating a segment"""
        seg = Segment(
            start=1.5,
            end=3.0,
            english_text="Hello world",
            irish_text="Dia dhuit domhan",
            index=1,
        )

        self.assertEqual(seg.start, 1.5)
        self.assertEqual(seg.end, 3.0)
        self.assertEqual(seg.english_text, "Hello world")
        self.assertEqual(seg.irish_text, "Dia dhuit domhan")

    def test_segment_duration(self):
        """Test duration calculation"""
        seg = Segment(start=1.0, end=4.5, english_text="Test", irish_text="Tástáil")
        self.assertEqual(seg.duration, 3.5)

    def test_segment_milliseconds(self):
        """Test millisecond conversions"""
        seg = Segment(start=1.5, end=3.0, english_text="Test", irish_text="Tástáil")

        self.assertEqual(seg.start_ms, 1500)
        self.assertEqual(seg.end_ms, 3000)
        self.assertEqual(seg.duration_ms, 1500)

    def test_male_marker_detection(self):
        """Test male voice marker detection"""
        seg_male = Segment(
            start=1.0, end=2.0, english_text="Male voice#", irish_text="Guth fir"
        )
        seg_female = Segment(
            start=1.0, end=2.0, english_text="Female voice", irish_text="Guth mná"
        )

        self.assertTrue(seg_male.has_male_marker())
        self.assertFalse(seg_female.has_male_marker())

    def test_clean_english_text(self):
        """Test removing voice markers from English text"""
        seg = Segment(
            start=1.0, end=2.0, english_text="Test text#", irish_text="Téacs tástála"
        )
        self.assertEqual(seg.get_clean_english_text(), "Test text")

    def test_empty_segment_detection(self):
        """Test empty segment detection"""
        seg_empty = Segment(start=1.0, end=2.0, english_text="Test", irish_text="")
        seg_whitespace = Segment(
            start=1.0, end=2.0, english_text="Test", irish_text="   "
        )
        seg_valid = Segment(
            start=1.0, end=2.0, english_text="Test", irish_text="Tástáil"
        )

        self.assertTrue(seg_empty.is_empty())
        self.assertTrue(seg_whitespace.is_empty())
        self.assertFalse(seg_valid.is_empty())


class TestDubbingJob(unittest.TestCase):
    """Test DubbingJob domain model"""

    def test_dubbing_job_creation(self):
        """Test creating a dubbing job"""
        job = DubbingJob(
            video_path=Path("video.mp4"),
            eng_srt_path=Path("eng.srt"),
            gael_srt_path=Path("gael.srt"),
            output_filename="output.mp4",
        )

        self.assertEqual(job.video_path, Path("video.mp4"))
        self.assertEqual(job.output_filename, "output.mp4")

    def test_current_folder_property(self):
        """Test current folder extraction"""
        job = DubbingJob(
            video_path=Path("/test/folder/video.mp4"),
            eng_srt_path=Path("eng.srt"),
            gael_srt_path=Path("gael.srt"),
            output_filename="output.mp4",
        )

        self.assertEqual(job.current_folder, Path("/test/folder"))

    def test_output_paths(self):
        """Test output path calculations"""
        job = DubbingJob(
            video_path=Path("/test/video.mp4"),
            eng_srt_path=Path("eng.srt"),
            gael_srt_path=Path("gael.srt"),
            output_filename="dubbed.mp4",
        )

        self.assertEqual(job.output_path, Path("/test/dubbed.mp4"))
        self.assertEqual(job.output_srt_english, Path("/test/subtitles_english.srt"))
        self.assertEqual(job.output_srt_irish, Path("/test/subtitles_irish.srt"))

    def test_from_paths_factory(self):
        """Test creating job from string paths"""
        job = DubbingJob.from_paths(
            "/test/video.mp4", "/test/eng.srt", "/test/gael.srt", "output.mp4"
        )

        self.assertIsInstance(job.video_path, Path)
        # Use Path comparison instead of string to handle Windows/Unix differences
        self.assertEqual(job.video_path, Path("/test/video.mp4"))


if __name__ == "__main__":
    unittest.main()
