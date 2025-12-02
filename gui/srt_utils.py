# srt_utils.py (copied from source, adjusted for package-relative helpers)

from .helpers import parse_time, format_srt_time


def load_and_combine_srt(eng_path, iri_path):
    eng_segments = parse_srt(eng_path)
    iri_segments = parse_srt(iri_path)
    if len(eng_segments) != len(iri_segments):
        print("Error: SRT files have mismatched segment counts.")
        exit()

    segments = []
    for i in range(len(eng_segments)):
        if (
            eng_segments[i]["start"] != iri_segments[i]["start"]
            or eng_segments[i]["end"] != iri_segments[i]["end"]
        ):
            print("Warning: Timings mismatch between SRT files.")
        segments.append(
            {
                "start": eng_segments[i]["start"],
                "end": eng_segments[i]["end"],
                "eng_text": eng_segments[i]["text"],
                "iri_text": iri_segments[i]["text"],
            }
        )
    return segments


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


def write_srt(file_path, entries, lang_key):
    with open(file_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(f"{entry['index']}\n")
            f.write(
                f"{format_srt_time(entry['start'])} --> {format_srt_time(entry['end'])}\n"
            )
            f.write(f"{entry[lang_key]}\n\n")
