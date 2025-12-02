"""
Centralized dubbing pipeline moved into `dubbing_core`.

This module adapts the logic previously present in `source/app_main.py` and
exposes `run_dubbing_process(...)` which performs the full workflow using
the helper modules located in `source/`.
"""

from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import os
import time
import glob
import shutil
import random

# Import helpers from the gui package (migrated from `source` into `gui`)
from gui.helpers import print_progress
from gui.abair_utils import set_abair_settings, get_abair_audio
from gui.srt_utils import load_and_combine_srt, write_srt
from gui.timing_utils import calculate_smart_timing, add_sync_silence
from gui.selenium_utils import setup_selenium


OUTPUT_SRT_ENGLISH = r"subtitles_english.srt"
OUTPUT_SRT_IRISH = r"subtitles_irish.srt"


def run_dubbing_process(video_path, eng_srt_path, gael_srt_path, output_filename):
    """Execute the entire dubbing pipeline.

    Args:
        video_path (str): Full path to input video
        eng_srt_path (str): Full path to English SRT
        gael_srt_path (str): Full path to Irish SRT
        output_filename (str): Desired output filename (placed next to input video)

    Returns:
        str: Status message (successful path or error message prefixed with 'ERROR:')
    """
    current_folder = os.path.dirname(os.path.abspath(video_path))

    # 1. Parse SRT files
    print("1. Parsing SRT files...")
    try:
        segments = load_and_combine_srt(eng_srt_path, gael_srt_path)
    except Exception as e:
        return f"ERROR: Failed to parse SRT files. Details: {e}"

    # 2. Load video
    print("2. Loading video...")
    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Error loading video: {e}")
        return f"ERROR: Failed to load video from {video_path}. Check if the file is valid."

    # 3. SETUP SELENIUM
    print("3. Setting up WebDriver...")
    try:
        driver, wait = setup_selenium(current_folder)
    except Exception as e:
        print(f"Error setting up Selenium: {e}")
        return f"ERROR: Failed to set up Chrome/Selenium. Ensure Chrome is installed and updated. Details: {e}"

    # Voice options
    voices = [
        {"dialect": "Kerry", "gender": "Female"},
        {"dialect": "Kerry", "gender": "Male"},
        {"dialect": "Connemara", "gender": "Female"},
    ]

    # 4. Dub Loop
    print("4. Dubbing...")

    dub_track = AudioSegment.silent(duration=0)
    srt_entries = []
    current_time_ms = 0
    previous_voice = None

    for i, seg in enumerate(segments):
        start_sec = seg["start"]
        end_sec = seg["end"]
        target_start_ms = int(start_sec * 1000)

        english_text = seg["eng_text"]
        irish_text = seg["iri_text"]

        if not irish_text:
            continue

        # Determine voice
        if english_text.endswith("#"):
            english_text = english_text[:-1]
            voice = random.choice([v for v in voices if v["gender"] == "Male"])
        else:
            voice = random.choice([v for v in voices if v["gender"] == "Female"])

        # Progress Bar for Dubbing
        print_progress(
            i + 1, len(segments), prefix="Dubbing:", suffix=f"Seg {i+1}", length=40
        )

        # === SMART TIMING LOGIC ===
        allowed_end_sec, final_duration = calculate_smart_timing(
            irish_text, start_sec, end_sec, i, segments, video.duration
        )
        # ==========================

        # Sync Silence
        gap_ms = target_start_ms - current_time_ms
        dub_track, current_time_ms = add_sync_silence(
            dub_track, target_start_ms, current_time_ms, i
        )
        if current_time_ms is None:  # Skip flag
            continue

        # Skip settings if voice unchanged
        if previous_voice == voice:
            pass
        else:
            if not set_abair_settings(driver, voice["dialect"], voice["gender"], wait):
                continue
            previous_voice = voice

        # Get Audio
        for old_file in glob.glob(os.path.join(current_folder, "synthesis*")):
            try:
                os.remove(old_file)
            except:
                pass

        audio_file = get_abair_audio(
            driver, irish_text, current_folder, voice["dialect"], voice["gender"], wait
        )

        if audio_file:
            voice_audio = AudioSegment.from_file(audio_file)
            # Speed up for Connemara Female to 140%
            if voice["dialect"] == "Connemara" and voice["gender"] == "Female":
                voice_audio = voice_audio.speedup(playback_speed=1.4)
            dub_track += voice_audio
            current_time_ms += len(voice_audio)

            # Add to SRT list (with cleaned english_text)
            srt_entries.append(
                {
                    "index": len(srt_entries) + 1,
                    "start": start_sec,
                    "end": allowed_end_sec,
                    "eng": english_text,
                    "iri": irish_text,
                }
            )

            # Clean up temp file
            try:
                if os.path.exists("temp_seg.mp3"):
                    os.remove("temp_seg.mp3")
                shutil.move(audio_file, "temp_seg.mp3")
            except:
                pass
        else:
            # Fallback silence
            dur = int((end_sec - start_sec) * 1000)
            if gap_ms > 0:
                dub_track += AudioSegment.silent(duration=dur)
                current_time_ms += dur

        time.sleep(5)  # Add delay between segments to prevent rushing

    # Clean up WebDriver
    driver.quit()

    # 5. Mixing & Export
    print("\n5. Muxing Final Video...")

    dub_track.export("dubbed_audio.wav", format="wav")

    new_audioclip = AudioFileClip("dubbed_audio.wav")
    final_video = video.with_audio(new_audioclip)

    output_path = os.path.join(os.path.dirname(video_path), output_filename)

    try:
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            preset="fast",
            logger=None,
        )
    except Exception as e:
        print(f"Error writing video: {e}")
        return f"ERROR: Failed to write final video file. Check file permissions or video codec. Error: {e}"

    # 6. Write SRTs
    print("6. Writing Subtitles...")

    output_srt_eng = os.path.join(os.path.dirname(video_path), OUTPUT_SRT_ENGLISH)
    output_srt_iri = os.path.join(os.path.dirname(video_path), OUTPUT_SRT_IRISH)

    write_srt(output_srt_eng, srt_entries, "eng")
    write_srt(output_srt_iri, srt_entries, "iri")

    # Cleanup
    for f in ["temp_seg.mp3"]:
        if os.path.exists(f):
            os.remove(f)

    print("\nDONE!")
    return f"Success! Output video saved as: {output_path}"
