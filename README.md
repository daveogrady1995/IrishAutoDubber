# Irish Auto-Dubber

An application for automatically dubbing videos from English to Irish using the Abair TTS service.

## Download

**Latest Release: v1.0.1**

- [Download Windows Installer](https://www.dropbox.com/scl/fi/7avq42mecshwrk4437j85/AbairDubbing_Setup_v5.exe?rlkey=oxhd5gccuu7zsv0lw3ihd2bh5&st=6k00kwsv&dl=0)
- [Download macOS Installer (.dmg)](https://www.dropbox.com/scl/fi/g35rkp3qy5tbltoy6e3m0/AbairDubbing-macOS.dmg?rlkey=b6k51uuoevdszn0zectweoly9&st=vht1mgc2&dl=0)

## About

This workspace contains the dubbing pipeline and two frontends (CLI and GUI).

Layout (important files/folders):

- `dubbing_core/` — Consolidated pipeline implementation. Call the public API `dubbing_core.run_dub(video, eng_srt, gael_srt, output_filename)`.
- `gui/` — GUI frontend and helper modules (new, migrated from `source/`). Run: `python -m gui.gui_app`.
- `cli/` — CLI shim that delegates to `irishautodub` (runs the same core pipeline).
- `source/` — Original GUI implementation (left in place as a backup). If you prefer, this folder can be archived or removed; an archived copy was created at `archive/source_backup/`.
- `irishautodub/` — Original CLI frontend (now delegates to `dubbing_core`).
- `archive/` — Archived files and backups.
- `.venv/` — Canonical virtualenv for running the project. Use `.\.venv\Scripts\python.exe` on Windows.

Quick commands

Run GUI:

```pwsh
.\.venv\Scripts\python.exe -m gui.gui_app
```

Run CLI:

```pwsh
.\.venv\Scripts\python.exe -m cli.dub_to_irish <video.mp4> <eng.srt> <gael.srt> output.mp4
```

Run import smoke-check:

```pwsh
.\.venv\Scripts\python.exe smoke2.py
```

## Building the Installer

### Windows Installer

To create a Windows installer for distribution:

#### Step 1: Build the Executable with PyInstaller

```pwsh
# Navigate to the app directory
cd <your-project-path>\app

# Build the executable using PyInstaller
.\.venv\Scripts\python.exe -m PyInstaller --clean AbairDubbing_onedir_v5.spec
```

This will create a folder `dist\AbairDubbing_onedir_v5\` containing the executable and all dependencies.

#### Step 2: Create the Installer with Inno Setup

```pwsh
# Compile the installer using Inno Setup
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "<your-project-path>\app\dist\InnoSetup\AbairDubbingInstaller.iss"
```

This will create `AbairDubbing_Setup_v5.exe` in `dist\InstallerOutput\`.

**Note**: Update the paths in `dist\InnoSetup\AbairDubbingInstaller.iss` to match your project location before running Inno Setup.

#### Build Configuration Files

- **PyInstaller spec**: `AbairDubbing_onedir_v5.spec` - Defines what gets bundled into the executable
- **Inno Setup script**: `dist/InnoSetup/AbairDubbingInstaller.iss` - Defines the installer behavior and shortcuts

### macOS Installer

To create a macOS DMG installer for distribution:

#### Step 1: Build the .app Bundle

```bash
# Make the build script executable
chmod +x build_macos.sh

# Run the build script
./build_macos.sh
```

This will create `dist/AbairDubbing.app` containing the application bundle.

#### Step 2: Create the DMG

```bash
# Make the DMG creation script executable
chmod +x create_dmg.sh

# Run the DMG creation script
./create_dmg.sh
```

This will create `dist/AbairDubbing-macOS-1.0.0.dmg` ready for distribution.

#### Build Configuration Files

- **PyInstaller spec**: `build_macos.spec` - Defines what gets bundled into the .app
- **Build script**: `build_macos.sh` - Automates the PyInstaller build process
- **DMG script**: `create_dmg.sh` - Creates the distributable DMG file

### Distribution

Upload the installer to Dropbox or your preferred file hosting service and update the download link in this README.

Notes

- End-to-end dubbing requires Chrome and network access to `https://abair.ie/synthesis`.
- `requirements.txt` is pinned from the `.venv` — regenerate it with `.\.venv\Scripts\python.exe -m pip freeze > requirements.txt` after making env changes.
