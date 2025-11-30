# See the AI Dubbing Software in Action

Check out this TikTok profile to see the AI dubbing software in action: [@bluey95883](https://www.tiktok.com/@bluey95883)

# ☘️ AutoIrishDubber

**AutoIrishDubber** is a Python-based console application designed to automatically dub an input video (`input.mp4`) into Irish (Gaeilge).

It leverages **Selenium** to automate speech synthesis on [Abair.ie](https://www.abair.ie/), generating dubbed audio segments that align with subtitle timings. It then mixes the new audio into an output video and produces updated subtitle files with adjusted timings.

---

## 🚀 Key Features

* **🎬 Input Parsing & Syncing**: Reads and synchronizes English and Irish SRT subtitles, ensuring segments match perfectly.
* **🗣️ Authentic Voice Selection**: Randomly selects between high-quality **Kerry dialect voices** (Male "Danny" or Female) or **Connemara Female** (AI model enabled).
* **⏱️ Smart Timing Logic**:
    * Adjusts subtitle durations based on text length and reading speed (~14 chars/sec).
    * Extends audio into silence gaps to avoid chopping.
    * Includes a skip threshold for lagged segments.
* **🤖 Selenium Automation**: Fully automates the interaction with Abair.ie (cookies, language switching, dialect/model selection, speed settings, synthesis, and file download). Includes robust retry logic and temp file cleanup.
* **🔊 Audio Processing**: Uses `pydub` to build a clean audio track, inserting synced silences and appending synthesized audio (with optional speed-up for specific voices).
* **🎞️ Video Muxing**: Uses `moviepy` to replace the original audio with the new Irish track, handling decoding errors gracefully.
* **📊 Progress Tracking**: Displays a console progress bar during the dubbing process.

---

## 🛠️ Installation

### 1. Prerequisites
* **Python**: Version **3.11.9** is recommended for compatibility.
* **FFmpeg**: Required by MoviePy. Download it from [ffmpeg.org](https://ffmpeg.org/download.html) and ensure it is added to your system PATH.
* **Google Chrome**: Required for Selenium automation.

### 2. Setup Virtual Environment
It is recommended to use a virtual environment to avoid dependency conflicts.

```bash
# Create the environment
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install moviepy pydub selenium webdriver-manager
```

## 📂 Project Structure

Place the following files in your root project folder:

| File              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| dub_to_irish.py   | Main Script. Run this to start the dubbing process.                         |
| abair_utils.py    | Utilities for interacting with Abair.ie.                                    |
| helpers.py        | General helpers (progress bars, time formatting).                           |
| srt_utils.py      | Parsers and writers for .srt subtitle files.                                |
| timing_utils.py   | Logic for smart timing calculation and sync.                                |
| selenium_utils.py | Boilerplate for setting up the Chrome WebDriver.                            |

## ⚙️ Usage & Workflow

### Step 1: Prepare Input Files

You must have the following three files in your project directory:

1. `input.mp4`: The video you want to dub.

2. `eng.srt`: The English subtitles.

3. `gael.srt`: The Irish translations (must match the timing of the English file).

💡 **Pro Tip: How to generate these files**

You can generate the SRT files using tools like CapCut or ClipChamp. Upload your video, use the auto-caption or auto-dub feature to generate subtitles, and export with the SRT file to get `eng.srt`.

1. **Translate**: Copy the content of `eng.srt` and ask Grok or Gemini to translate it to Irish (or use Google Translate or DeepL).

2. **Save**: Save the translated file as `gael.srt`, ensuring the timings match the English file.

### Step 2: Run the Script

Execute the main script via the console:
```bash
python dub_to_irish.py
```

### Step 3: Outputs

Upon completion, the script generates:

* `dubbed_kerry_reverted.mp4`: The final video with Irish audio.

* `dubbed_audio.wav`: The standalone dubbed audio track (for reference).

* `subtitles_english.srt` & `subtitles_irish.srt`: New subtitle files with timings adjusted to match the spoken Irish audio.

## 🎥 Post-Processing (CapCut Studio)

The generated subtitle files are optimized for video editing software like CapCut.

1. Open your project in CapCut Studio.

2. Import `dubbed_kerry_reverted.mp4`.

3. Drag `subtitles_english.srt` or `subtitles_irish.srt` onto the timeline.

4. Result: They will align automatically with the new video timings!

## 📝 Configuration & Notes

* **Voice Customization**: You can modify the specific voices used by editing the `voices` list inside `dub_to_irish.py`.

* **Performance**: Selenium relies on the live Abair.ie website. Long texts or network delays may extend runtime. The script includes built-in waits (2-5 seconds) to mitigate errors.

* **Work in Progress**: The output filename (`dubbed_kerry_reverted.mp4`) is currently hardcoded but can be changed in the main script.
