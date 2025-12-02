"""helpers.py (copied from `source/helpers.py`) for the new `gui` package."""

import datetime
import glob
import os
import sys


# --- CONSOLE HELPER: PROGRESS BAR ---
def print_progress(
    iteration, total, prefix="", suffix="", decimals=1, length=50, fill="█"
):
    """Call in a loop to create terminal progress bar"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r{prefix} |{bar}| {percent}% {suffix}")
    sys.stdout.flush()
    if iteration == total:
        print()


def format_srt_time(seconds):
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - total_seconds) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def parse_time(time_str):
    hours, minutes, secs_millis = time_str.split(":")
    secs, millis = secs_millis.split(",")
    return (
        float(hours) * 3600 + float(minutes) * 60 + float(secs) + float(millis) / 1000
    )


def parse_srt(file_path):
    segments = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.isdigit():
            index = int(line)
            time_line = lines[i + 1].strip()
            start_str, end_str = time_line.split(" --> ")
            start = parse_time(start_str)
            end = parse_time(end_str)
            text = ""
            i += 2
            while i < len(lines) and lines[i].strip() != "":
                text += lines[i].strip() + " "
                i += 1
            text = text.strip()
            segments.append({"start": start, "end": end, "text": text})
        else:
            i += 1
    return segments


def get_latest_file(folder):
    files = glob.glob(os.path.join(folder, "*"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)
