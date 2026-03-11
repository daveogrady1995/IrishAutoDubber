"""
Auto-transcription and translation service.

Uses faster-whisper (large-v3) to transcribe English audio from a video,
then translates each segment to Irish using facebook/nllb-200-distilled-600M.
Produces temporary English and Irish SRT files ready for the dubbing pipeline.
"""

import os


def _seconds_to_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_srt_files(video_path: str, output_dir: str) -> tuple[str, str]:
    """
    Transcribe a video's English audio and translate it to Irish.

    Args:
        video_path:  Absolute path to the input video file.
        output_dir:  Directory where the temporary SRT files will be written.

    Returns:
        (eng_srt_path, gael_srt_path) — paths to the generated SRT files.
    """
    from moviepy import VideoFileClip
    from faster_whisper import WhisperModel
    from transformers import pipeline as hf_pipeline

    audio_path = os.path.join(output_dir, "_auto_temp_audio.wav")

    # --- 1. Extract audio ---
    print("[AutoDub] Extracting audio from video...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, fps=16000, logger=None)
    video.close()

    # --- 2. Transcribe with Whisper large-v3 ---
    print("[AutoDub] Loading Whisper large-v3 model (first run downloads ~1.5 GB)...")
    whisper_model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    print("[AutoDub] Transcribing...")
    raw_segments, _ = whisper_model.transcribe(audio_path, language="en", beam_size=5)
    segments = list(raw_segments)
    print(f"[AutoDub] Transcribed {len(segments)} segments.")

    # --- 3. Translate EN → Irish with NLLB-200 ---
    print("[AutoDub] Loading NLLB-200 translation model...")
    translator = hf_pipeline(
        "translation",
        model="facebook/nllb-200-distilled-600M",
        src_lang="eng_Latn",
        tgt_lang="gle_Latn",
    )

    eng_blocks: list[str] = []
    gael_blocks: list[str] = []

    for i, seg in enumerate(segments, 1):
        start_ts = _seconds_to_srt_time(seg.start)
        end_ts = _seconds_to_srt_time(seg.end)
        eng_text = seg.text.strip()

        print(f"[AutoDub] Translating segment {i}/{len(segments)}...")
        irish_result = translator(eng_text, max_length=512)
        irish_text = irish_result[0]["translation_text"]

        eng_blocks.append(f"{i}\n{start_ts} --> {end_ts}\n{eng_text}")
        gael_blocks.append(f"{i}\n{start_ts} --> {end_ts}\n{irish_text}")

    # --- 4. Write SRT files ---
    eng_srt_path = os.path.join(output_dir, "_auto_eng.srt")
    gael_srt_path = os.path.join(output_dir, "_auto_gael.srt")

    with open(eng_srt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(eng_blocks) + "\n")

    with open(gael_srt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(gael_blocks) + "\n")

    # --- 5. Cleanup temp audio ---
    try:
        os.remove(audio_path)
    except OSError:
        pass

    print(f"[AutoDub] SRT files written: {eng_srt_path}, {gael_srt_path}")
    return eng_srt_path, gael_srt_path
