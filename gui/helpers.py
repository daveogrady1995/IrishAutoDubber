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


# --- LANGUAGE SELECTOR HELPER ---
import tkinter as tk
from gui.localization import get_localization


def create_language_selector(parent, colors, on_language_change):
    """Create a language selector dropdown"""
    loc = get_localization()

    selector_frame = tk.Frame(parent, bg=colors["bg"])

    # Language label
    lang_label = tk.Label(
        selector_frame,
        text="🌐",
        font=("SF Pro Text", 16),
        bg=colors["bg"],
        fg=colors["text"],
    )
    lang_label.pack(side="left", padx=(0, 8))

    # Language variable
    lang_var = tk.StringVar(value=loc.get_current_language())

    # Create custom styled option menu
    lang_options = [
        ("English", "en"),
        ("Gaeilge", "ga"),
    ]

    def change_language(lang_code):
        on_language_change(lang_code)

    # Create buttons for language selection
    for lang_name, lang_code in lang_options:
        is_current = lang_code == loc.get_current_language()

        btn = tk.Button(
            selector_frame,
            text=lang_name,
            command=lambda lc=lang_code: change_language(lc),
            font=("SF Pro Text", 11, "bold" if is_current else "normal"),
            bg=colors["primary"] if is_current else colors["card"],
            fg="white" if is_current else colors["text"],
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        )
        btn.pack(side="left", padx=2)

    return selector_frame
