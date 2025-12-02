# timing_utils.py (copied from source)
from pydub import AudioSegment

LONG_TEXT_THRESHOLD = 60  # Characters
CHARS_PER_SEC_READING_SPEED = 14  # Average reading speed
SKIP_THRESHOLD_SEC = 2.5


def calculate_smart_timing(irish_text, start_sec, end_sec, i, segments, video_duration):
    char_count = len(irish_text)
    min_reading_time_sec = char_count / CHARS_PER_SEC_READING_SPEED
    if char_count > LONG_TEXT_THRESHOLD:
        min_reading_time_sec += 1.5

    original_duration = end_sec - start_sec
    final_duration = max(original_duration, min_reading_time_sec)

    # Look ahead to next segment to avoid overlap
    next_start_sec = (
        segments[i + 1]["start"] if (i + 1 < len(segments)) else video_duration
    )
    # Extend subtitle into the silence gap if needed
    allowed_end_sec = min(start_sec + final_duration, next_start_sec - 0.1)

    return allowed_end_sec, final_duration


def add_sync_silence(dub_track, target_start_ms, current_time_ms, i):
    gap_ms = target_start_ms - current_time_ms
    if gap_ms > 0:
        dub_track += AudioSegment.silent(duration=gap_ms)
        current_time_ms += gap_ms
    elif gap_ms < -(SKIP_THRESHOLD_SEC * 1000):
        print(f"\n   > Skipping segment {i+1} due to lag.")
        return dub_track, None  # Flag to skip
    return dub_track, current_time_ms
