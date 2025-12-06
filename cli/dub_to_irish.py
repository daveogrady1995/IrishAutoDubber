"""CLI entrypoint for the dubbing pipeline.

This lets users run `python -m cli.dub_to_irish <video> <eng_srt> <gael_srt> <output>`.
"""

import sys
from dubbing_core import run_dub


def main():
    """CLI entry point for dubbing."""
    if len(sys.argv) < 5:
        print("Usage: python -m cli.dub_to_irish <video.mp4> <eng.srt> <gael.srt> <output.mp4>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    eng_srt_path = sys.argv[2]
    gael_srt_path = sys.argv[3]
    output_filename = sys.argv[4]
    
    print(f"Starting dubbing process...")
    print(f"  Video: {video_path}")
    print(f"  English SRT: {eng_srt_path}")
    print(f"  Irish SRT: {gael_srt_path}")
    print(f"  Output: {output_filename}")
    print()
    
    result = run_dub(video_path, eng_srt_path, gael_srt_path, output_filename)
    
    if result.startswith("ERROR:"):
        print(f"\n{result}")
        sys.exit(1)
    else:
        print(f"\n{result}")
        sys.exit(0)


if __name__ == "__main__":
    main()
