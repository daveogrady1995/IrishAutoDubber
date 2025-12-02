# dub_to_irish.py - CLI entry that delegates to the consolidated dubbing_core

import os
import sys
from typing import Optional

INPUT_VIDEO = r"input.mp4"
OUTPUT_VIDEO = r"dubbed_kerry_reverted.mp4"

# SRT filenames
SRT_ENGLISH = r"eng.srt"
SRT_IRISH = r"gael.srt"

# Output filenames
OUTPUT_SRT_ENGLISH = r"subtitles_english.srt"
OUTPUT_SRT_IRISH = r"subtitles_irish.srt"


def run_dubbing_pipeline(
    video_path: Optional[str] = None,
    eng_srt_path: Optional[str] = None,
    gael_srt_path: Optional[str] = None,
    output_filename: Optional[str] = None,
):
    """CLI-friendly wrapper that delegates to `dubbing_core.run_dub`.

    If any argument is None the function falls back to the previous
    default constants so the script remains backwards compatible.
    """
    from dubbing_core import run_dub

    v = video_path or INPUT_VIDEO
    e = eng_srt_path or SRT_ENGLISH
    g = gael_srt_path or SRT_IRISH
    out = output_filename or OUTPUT_VIDEO

    return run_dub(v, e, g, out)


if __name__ == "__main__":
    # Usage:
    #   python dub_to_irish.py <video_path> <eng_srt> <gael_srt> [output_filename]
    if len(sys.argv) >= 4:
        video_arg = sys.argv[1]
        eng_arg = sys.argv[2]
        gael_arg = sys.argv[3]
        out_arg = sys.argv[4] if len(sys.argv) >= 5 else None
        result = run_dubbing_pipeline(video_arg, eng_arg, gael_arg, out_arg)
    else:
        print("No CLI args provided — falling back to defaults in file.")
        result = run_dubbing_pipeline()

    print(result)
