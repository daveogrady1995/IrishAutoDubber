"""Packaging helpers for locating bundled resources at runtime.

When the application is frozen by PyInstaller, resources are unpacked into
`sys._MEIPASS`. Use `resource_path` to locate bundled files both when
running from source and when running from a frozen executable.
"""

import os
import sys


def resource_path(relpath: str) -> str:
    """Return an absolute path to a resource bundled with the application.

    Args:
        relpath: Path relative to the project root or to the packaged bundle.

    Returns:
        Absolute filesystem path to the resource.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # When running from source, base is repository apps folder
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, relpath)
