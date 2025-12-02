"""
Minimal shared wrapper for the dubbing pipeline.

This module exposes `run_dub(...)` which delegates to the GUI-friendly
`source.app_main.run_dubbing_process` implementation when available.

The wrapper is intentionally non-invasive: it does not move code, it only
provides a stable import path for frontends (GUI/CLI) to call the core
pipeline from a single place.
"""

from typing import Optional

from .core import run_dubbing_process as _run_dubbing_process


def run_dub(
    video_path: str, eng_srt_path: str, gael_srt_path: str, output_filename: str
) -> str:
    """Run the dubbing pipeline via the consolidated core implementation.

    This calls the implementation in `dubbing_core.core` and returns
    the same status string as the original `run_dubbing_process`.
    """
    try:
        return _run_dubbing_process(
            video_path, eng_srt_path, gael_srt_path, output_filename
        )
    except Exception as e:
        raise RuntimeError(f"dubbing_core.run_dub failed: {e}")
