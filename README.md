# ☘️ AutoIrishDubber

![AutoIrishDubber Screenshot](https://github.com/daveogrady1995/IrishAutoDubber/blob/main/screenshot.png?raw=true)

**AutoIrishDubber** is a Python-based application designed to automatically dub videos from English into Irish (Gaeilge). It leverages **Selenium** to automate speech synthesis on [Abair.ie](https://www.abair.ie/), generating dubbed audio segments that align with subtitle timings, then mixes the new audio into an output video with adjusted subtitles.

---

## 📥 Download

**Latest Release: v1.0.1**

- [Download Windows Installer](https://www.dropbox.com/scl/fi/7avq42mecshwrk4437j85/AbairDubbing_Setup_v5.exe?rlkey=oxhd5gccuu7zsv0lw3ihd2bh5&st=vifiabfk&dl=1)
- [Download macOS Installer (.dmg)](https://www.dropbox.com/scl/fi/9uts1oawo4popp6yv4iq8/AbairDubbing-macOS.dmg?rlkey=ei3wthbcqnh2qzfnx5ub7nscf&st=jy743r86&dl=1)

**Installation**: Download and run the installer for your platform. It will create shortcuts for easy access. No Python installation required for end users!

### macOS Security Note

When first opening the app on macOS, you may see a security warning because the app isn't signed with an Apple Developer certificate. To approve it:

1. Try to open `AbairDubbing.app`
2. If blocked, go to **System Settings** → **Privacy & Security**
3. Scroll down to the **Security** section
4. Click **"Open Anyway"** next to the message about the blocked app
5. Confirm by clicking **"Open"** in the dialog

Alternatively, right-click the app and select **"Open"**, then click **"Open"** in the security dialog.

**If the above methods don't work**, open Terminal and run:
```bash
xattr -d com.apple.quarantine /Applications/AbairDubbing.app
```

---

## 🎬 See It In Action

Check out this TikTok profile to see the AI dubbing software in action: [@bluey95883](https://www.tiktok.com/@bluey95883)

---

## 🚀 Key Features

- **🎬 Input Parsing & Syncing**: Reads and synchronizes English and Irish SRT subtitles, ensuring segments match perfectly.
- **🗣️ Authentic Voice Selection**: Randomly selects between high-quality **Kerry dialect voices** (Male "Danny" or Female) with natural-sounding synthesis.
- **⏱️ Smart Timing Logic**:
  - Adjusts subtitle durations based on text length and reading speed (~14 chars/sec).
  - Extends audio into silence gaps to avoid chopping.
  - Includes a skip threshold for lagged segments.
- **🤖 Selenium Automation**: Fully automates the interaction with Abair.ie (cookies, language switching, dialect/model selection, speed settings, synthesis, and file download). Includes robust retry logic and temp file cleanup.
- **🔊 Audio Processing**: Uses `pydub` to build a clean audio track, inserting synced silences and appending synthesized audio (with optional speed-up for specific voices).
- **🎞️ Video Muxing**: Uses `moviepy` to replace the original audio with the new Irish track, handling decoding errors gracefully.
- **🖥️ Modern GUI**: User-friendly graphical interface with Material Design styling for easy video dubbing.
- **📊 Progress Tracking**: Displays real-time progress during the dubbing process.

---

## 🎯 Quick Start (For End Users)

1. **Download** the Windows installer from the link above
2. **Install** by running the setup executable
3. **Launch** the application from your desktop or start menu
4. **Prepare your files**:
   - Your video file (MP4, AVI, MOV, etc.)
   - English subtitles (`.srt` file)
   - Irish subtitles (`.srt` file) - see tips below on how to generate these
5. **Use the GUI** to select your files and click "Start Dubbing"
6. **Wait** for the process to complete - progress will be shown in real-time
7. **Find your output** in the same folder as your input video

### 💡 Pro Tip: Generating Subtitle Files

You can generate the required SRT files using tools like **CapCut** or **ClipChamp**:

1. Upload your video to CapCut/ClipChamp
2. Use the auto-caption feature to generate English subtitles
3. Export with the SRT file to get `eng.srt`
4. Copy the content of `eng.srt` and use **Grok**, **Gemini**, **ChatGPT**, or **Google Translate** to translate it to Irish
5. Save the translated file as `gael.srt`, ensuring the timings match the English file

---

## 🛠️ Developer Setup

This workspace contains the dubbing pipeline and two frontends (CLI and GUI).

### Prerequisites

- **Python**: Version **3.11.9** is recommended for compatibility.
- **FFmpeg**: Required by MoviePy. Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your system PATH.
- **Google Chrome**: Required for Selenium automation.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/daveogrady1995/IrishAutoDubber.git
   cd IrishAutoDubber/app
   ```

2. **Create and activate virtual environment**:

   ```bash
   # Windows:
   python -m venv .venv
   .\.venv\Scripts\activate

   # Mac/Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Project Structure

- `dubbing_core/` — Core dubbing pipeline. API: `run_dubbing_process(video, eng_srt, gael_srt, output_filename)`
- `gui/` — Modern GUI frontend with Material Design (tkinter-based)
- `cli/` — Command-line interface for batch processing
- `.venv/` — Python virtual environment for development
- `requirements.txt` — Pinned dependencies

### Quick Commands

**Run GUI**:

```bash
.\.venv\Scripts\python.exe run_gui.py
```

**Run CLI**:

```bash
.\.venv\Scripts\python.exe -m cli.dub_to_irish <video.mp4> <eng.srt> <gael.srt> output.mp4
```

**Run import smoke-check**:

```bash
.\.venv\Scripts\python.exe smoke2.py
```

---

## 📦 Building the Installer

To create a Windows installer for distribution:

### Step 1: Build the Executable with PyInstaller

```bash
# Navigate to the app directory
cd app

# Build the executable using PyInstaller
.\.venv\Scripts\python.exe -m PyInstaller --clean AbairDubbing_onedir_v5.spec
```

This creates `dist\AbairDubbing_onedir_v5\` containing the executable and all dependencies.

### Step 2: Create the Installer with Inno Setup

```bash
# Compile the installer using Inno Setup
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "dist\InnoSetup\AbairDubbingInstaller.iss"
```

This creates `AbairDubbing_Setup_v5.exe` in `dist\InstallerOutput\`.

### Step 3: Distribute

Upload the installer to Dropbox or your preferred file hosting service and update the download link in this README.

### Build Configuration Files

- **PyInstaller spec**: `AbairDubbing_onedir_v5.spec` - Defines what gets bundled into the executable
- **Inno Setup script**: `dist/InnoSetup/AbairDubbingInstaller.iss` - Defines the installer behavior and shortcuts

---

## 🎥 Post-Processing (CapCut Studio)

The generated subtitle files are optimized for video editing software like CapCut.

1. Open your project in CapCut Studio
2. Import the dubbed video output
3. Drag `subtitles_english.srt` or `subtitles_irish.srt` onto the timeline
4. Result: They will align automatically with the new video timings!

---

## 📝 Configuration & Notes

- **Voice Customization**: You can modify the specific voices used by editing the `voices` list inside `dubbing_core/core.py`.
- **Performance**: Selenium relies on the live Abair.ie website. Long texts or network delays may extend runtime. The script includes built-in waits (2-5 seconds) to mitigate errors.
- **Chrome Requirement**: End-to-end dubbing requires Chrome and network access to `https://abair.ie/synthesis`.
- **Temp Files**: All temporary files are now written to the system temp directory to avoid permission issues.

---

## 📄 Outputs

Upon completion, the application generates:

- **Dubbed video**: Your specified output filename with Irish audio
- **Subtitles**: `subtitles_english.srt` & `subtitles_irish.srt` with timings adjusted to match the spoken Irish audio

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the software.

---

## 📜 License

This project is open-source. Please ensure you comply with Abair.ie's terms of service when using their synthesis service.

---

## 🙏 Credits

- **Abair.ie**: For providing the Irish TTS synthesis service
- **MoviePy**: For video processing capabilities
- **Pydub**: For audio manipulation
- **Selenium**: For web automation

---

**Made with ☘️ for the Irish language community**
