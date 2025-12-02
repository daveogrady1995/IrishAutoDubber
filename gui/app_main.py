"""
Thin wrapper in `gui.app_main` that delegates to `dubbing_core`.
This mirrors the previous `source.app_main` behavior but lives under `gui`.
"""

from dubbing_core import run_dub


def run_dubbing_process(video_path, eng_srt_path, gael_srt_path, output_filename):
    return run_dub(video_path, eng_srt_path, gael_srt_path, output_filename)
