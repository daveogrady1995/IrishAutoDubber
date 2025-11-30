# dub_to_irish.py
# FEATURES: Console App + Smart Timing + Transcription Progress (NO DEMUCS)

from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import os
import time
import glob
import shutil
import random

# Import from separate files
from helpers import print_progress
from abair_utils import set_abair_settings, get_abair_audio
from srt_utils import load_and_combine_srt, write_srt
from timing_utils import calculate_smart_timing, add_sync_silence
from selenium_utils import setup_selenium

# ================== EDIT THESE ==================
INPUT_VIDEO = r"input.mp4"
OUTPUT_VIDEO = r"dubbed_kerry_reverted.mp4"

# SRT filenames
SRT_ENGLISH = r"eng.srt"
SRT_IRISH = r"gael.srt"

# Output filenames
OUTPUT_SRT_ENGLISH = r"subtitles_english.srt"
OUTPUT_SRT_IRISH = r"subtitles_irish.srt"


# =========================================================
# === ORIGINAL LOGIC WRAPPED IN FUNCTION ===
# =========================================================
def run_dubbing_pipeline():
    current_folder = os.getcwd()

    # Parse SRT files
    print("1. Parsing SRT files...")
    segments = load_and_combine_srt(SRT_ENGLISH, SRT_IRISH)
    print(f"   > Parsed {len(segments)} segments.")

    # Load video for duration
    print("2. Loading video...")
    try:
        video = VideoFileClip(INPUT_VIDEO)
        total_duration = video.duration
    except Exception as e:
        print(f"Error loading video: {e}")
        exit()

    # --- SETUP SELENIUM (ONLY ONCE) ---
    driver, wait = setup_selenium(current_folder)

    # Voice options
    voices = [
        {"dialect": "Kerry", "gender": "Female"},
        {"dialect": "Kerry", "gender": "Male"},
        {"dialect": "Connemara", "gender": "Female"},
    ]

    # Dub Loop
    print("4. Dubbing...")

    dub_track = AudioSegment.silent(duration=0)
    srt_entries = []
    current_time_ms = 0
    previous_voice = None  # Track to skip redundant settings

    for i, seg in enumerate(segments):
        start_sec = seg["start"]
        end_sec = seg["end"]
        target_start_ms = int(start_sec * 1000)

        english_text = seg["eng_text"]
        irish_text = seg["iri_text"]

        if not irish_text:
            continue

        # Determine voice based on english_text ending with "#"
        if english_text.endswith("#"):
            english_text = english_text[:-1]  # Remove the "#"
            voice = random.choice([v for v in voices if v["gender"] == "Male"])
        else:
            voice = random.choice([v for v in voices if v["gender"] == "Female"])

        # Progress Bar for Dubbing
        print_progress(
            i + 1, len(segments), prefix="Dubbing:", suffix=f"Seg {i+1}", length=40
        )

        print(f"\n   > Using voice: {voice['dialect']} {voice['gender']}")

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
            print("   > Voice unchanged from previous, skipping settings.")
        else:
            if not set_abair_settings(driver, voice["dialect"], voice["gender"], wait):
                # If settings fail, fallback or continue
                continue
            previous_voice = voice  # Update after successful set

        # Get Audio (settings already handled)
        # Clean old files (moved here if skipping settings)
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

            # Move/Rename temp file to keep folder clean
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

    driver.quit()

    # Mixing & Export
    print("\n5. Muxing Final Video...")

    # EXPORT ONLY THE DUB TRACK (No Background Music Mixing)
    dub_track.export("dubbed_audio.wav", format="wav")

    new_audioclip = AudioFileClip("dubbed_audio.wav")
    final_video = video.with_audio(new_audioclip)  # Use with_audio for robustness

    try:
        final_video.write_videofile(
            OUTPUT_VIDEO,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            preset="fast",
            logger=None,
        )
    except Exception as e:
        print(f"Error writing video: {e}")

    # Write SRTs
    print("6. Writing Subtitles...")
    write_srt(OUTPUT_SRT_ENGLISH, srt_entries, "eng")
    write_srt(OUTPUT_SRT_IRISH, srt_entries, "iri")

    # Cleanup (keep dubbed_audio.wav)
    for f in ["temp_seg.mp3"]:
        if os.path.exists(f):
            os.remove(f)

    print("\nDONE! Generated:")
    print(f"1. {OUTPUT_VIDEO}")
    print(f"2. {OUTPUT_SRT_ENGLISH}")
    print(f"3. {OUTPUT_SRT_IRISH}")
    print(f"4. dubbed_audio.wav (kept for reference)")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    run_dubbing_pipeline()
