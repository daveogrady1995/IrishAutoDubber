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
* **Python**: Version **3.11.9** is recommended for compatibility. To install Python 3.11.9, download it from the official Python website and follow the platform-specific steps below. This version is a bugfix release in the 3.11 series, so the installation process is similar to other 3.11.x versions. Note that Python 3.11 is no longer the latest major release (as of 2025, 3.13 and 3.14 are available), but you can install older versions like this for compatibility reasons. After installation, verify the version with `python3.11 --version` or `python --version` (depending on how it's aliased).

  #### Windows
  1. Download the 64-bit installer (recommended for most users) from: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe  
     (For 32-bit systems, use: https://www.python.org/ftp/python/3.11.9/python-3.11.9.exe. For ARM64, use the experimental: https://www.python.org/ftp/python/3.11.9/python-3.11.9-arm64.exe.)
     
  2. Run the `.exe` file as an administrator.

  3. In the installer wizard:
     - Check the box for "Add python.exe to PATH" (this is crucial for command-line access).
     - Select "Install for all users" if desired.
     - Click "Install Now" or customize the installation path if needed.

  4. Once complete, open Command Prompt and run `python --version` to confirm it's 3.11.9.

  If you encounter issues, refer to the official Windows Python docs for troubleshooting.

  #### macOS
  1. Download the installer package from: https://www.python.org/ftp/python/3.11.9/python-3.11.9-macos11.pkg  
     (This is a universal installer for macOS 10.9 and later, including Intel and Apple Silicon.)

  2. Double-click the `.pkg` file to launch the installer.

  3. Follow the on-screen prompts:
     - Agree to the license.
     - Choose the install location (default is fine).
     - Complete the installation.

  4. After installation, open Terminal and run `python3 --version` (or `python3.11 --version` if multiple versions are installed) to verify.

  Alternatively, if you prefer Homebrew (a package manager for macOS), you can install Python 3.11 via `brew install python@3.11`, but this may give you the latest patch in the 3.11 series (e.g., 3.11.10+). For the exact 3.11.9, stick to the official installer. If using Homebrew, you may need to update your PATH or alias `python3` to point to the new version.

  #### Linux (Ubuntu Focus)
  Ubuntu's default package manager (`apt`) often provides a different Python version depending on your release (e.g., Ubuntu 22.04 has 3.10, 24.04 has 3.12). To install exactly 3.11.9, use the Deadsnakes PPA (a third-party repository for older Python versions) or compile from source.

  ##### Using Deadsnakes PPA (Easiest for Ubuntu 20.04+)
  1. Open Terminal and add the PPA:  
     ```
     sudo add-apt-repository ppa:deadsnakes/ppa
     sudo apt update
     ```

  2. Install Python 3.11:  
     ```
     sudo apt install python3.11
     ```
     (This should give you 3.11.9 or the latest patch; check with `python3.11 --version`. If not exact, proceed to compiling from source.)

  3. Optionally install pip and venv:  
     ```
     sudo apt install python3.11-venv python3.11-dev
     ```

  ##### Compiling from Source (For Exact Version on Any Linux Distro)
  1. Download the source tarball: https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz

  2. Install build dependencies (on Ubuntu/Debian):  
     ```
     sudo apt update
     sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
     ```

  3. Extract and compile:  
     ```
     tar -xf Python-3.11.9.tgz
     cd Python-3.11.9
     ./configure --enable-optimizations
     make -j $(nproc)
     sudo make altinstall  # Use 'altinstall' to avoid overwriting system Python
     ```

  4. Verify: `python3.11 --version`

  For other Linux distros (e.g., Fedora, Arch), use their package managers (e.g., `dnf install python3.11` on Fedora) or adapt the source compile steps.

  **Additional Tips**:
  - **Multiple Versions**: If you have other Python versions installed, use tools like `pyenv` or virtual environments (`python -m venv`) to manage them without conflicts.
  - **Verify Installation**: Always run `python3.11 --version` (or the alias you set) to confirm.
  - **Why 3.11.9?**: If this is for the AutoIrishDubber project, it's recommended for compatibility, but newer 3.11.x patches should work similarly.

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
