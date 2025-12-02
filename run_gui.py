"""Tiny launcher for the GUI used by PyInstaller and local runs.

This keeps the module import explicit and is the target for the PyInstaller build.
"""

from gui.gui_app import main


if __name__ == "__main__":
    main()
