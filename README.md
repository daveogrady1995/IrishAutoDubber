# IrishAutoDubber
This script is a Python-based console application designed to dub an input video (`input.mp4`) into Irish audio using paired English and Irish subtitle files (`eng.srt` and `gael.srt`). It leverages Selenium to automate speech synthesis on the Abair.ie website, generating dubbed audio segments that align with subtitle timings, and then muxes the new audio into an output video (`dubbed_kerry_reverted.mp4`). It also produces updated subtitle files with adjusted timings (`subtitles_english.srt` and `subtitles_irish.srt`), and keeps the dubbed audio track (`dubbed_audio.wav`) for reference.

### Key Features:
- **Input Parsing**: Reads and syncs English and Irish SRT subtitles, ensuring matching segments.
- **Voice Selection**: Randomly chooses between Kerry dialect voices (Male "Danny" or Female) at 100% speed, with AI model enabled.
- **Smart Timing**: Adjusts subtitle durations based on text length and reading speed (14 chars/sec), extending into silence gaps to avoid overlaps, with a skip threshold for lagged segments.
- **Selenium Automation**: Sets up Chrome to interact with Abair.ie—handles cookies, language switch to Irish, dialect/gender/voice/model/speed settings, text input, synthesis, and audio download. Includes retries, delays (e.g., 2-5 seconds between actions), and cleanup of temp files to prevent overlaps.
- **Audio Processing**: Uses pydub to build a silent-initialized track, inserts synced silence gaps, appends synthesized audio segments, and exports as WAV.
- **Video Muxing**: Employs moviepy to replace the original video audio with the dubbed track, handling potential decoding errors gracefully.
- **Progress & Output**: Displays a console progress bar during dubbing, writes adjusted SRTs, cleans up temps (except dubbed audio), and logs completion.
- **Dependencies**: moviepy, pydub, selenium (with ChromeDriver), and standard libs like os, time, glob.

### Usage Notes:
- Edit file paths and settings at the top.
- Run via `python script.py`; requires Chrome and dependencies installed.
- Potential Issues: Selenium may need adjustments for site changes; long texts or network delays could extend runtime (built-in waits help mitigate rushing/overlaps).

For your project, this could serve as a core dubbing pipeline—extend it for batch processing, error logging, or integration with other TTS services if needed! If you need a more detailed breakdown or modifications, let me know.
