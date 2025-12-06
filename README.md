# Irish Auto-Dubber

An application for automatically dubbing videos from English to Irish using the Abair TTS service.

## Download

**Latest Release: v1.0.1**
- [Download Windows Installer](https://www.dropbox.com/scl/fi/zs4yxmtigltysru8j0iy1/AbairDubbing_Setup_v5.exe?rlkey=c6z6b90f8584eyc76s4pwjz02&st=rzgcdwxh&dl=0)

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

Notes

- End-to-end dubbing requires Chrome and network access to `https://abair.ie/synthesis`.
- `requirements.txt` is pinned from the `.venv` — regenerate it with `.\.venv\Scripts\python.exe -m pip freeze > requirements.txt` after making env changes.

If you want, I can now: (A) remove the `source/` folder, (B) leave it and only keep `archive/source_backup/`, or (C) create a git branch/tag for this migration. Tell me which you prefer.
