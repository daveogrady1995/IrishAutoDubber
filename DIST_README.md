AbairDubbing distribution

Included:
- `AbairDubbing_onedir/` directory contains the application and required data.
- `AbairDubbing_onedir.exe` is the GUI launcher (Windows).
- `drivers/chromedriver.exe` is included and used by default.

Notes:
- Chrome must be installed on the target machine. The included `chromedriver.exe` must be compatible with the installed Chrome version. If the GUI reports driver/Chrome mismatch, replace `drivers/chromedriver.exe` with a matching version.
- The bundled FFmpeg binary (`imageio-ffmpeg`) is included for media operations.
- For easier troubleshooting, use the `--onedir` build (this directory) instead of the single-file EXE.

How to run:
1. Extract the zip (if distributed as zip).
2. Run `AbairDubbing_onedir.exe`.

Optional: update the `drivers/chromedriver.exe` if you need to match a newer Chrome.
