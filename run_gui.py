"""Tiny launcher for the GUI used by PyInstaller and local runs.

This keeps the module import explicit and is the target for the PyInstaller build.
"""

import sys
import os
import platform
import warnings

# macOS-specific fixes (Windows uses defaults - no changes needed)
if platform.system() == "Darwin":
    # Fix OpenMP duplicate library issue on macOS
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    
    # Disable tokenizers parallelism to avoid fork deadlocks in GUI
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # Suppress huggingface_hub deprecation warning (safe to ignore)
    warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub")
    
    # Suppress macOS NSOpenPanel warning
    import io
    _stderr_backup = sys.stderr
    sys.stderr = io.StringIO()

from gui.gui_app import main


if __name__ == "__main__":
    # Restore stderr after initial imports
    if platform.system() == "Darwin":
        sys.stderr = _stderr_backup
    
    print("=" * 60)
    print("Abair Irish Auto-Dubbing Application")
    print("=" * 60)
    print("Starting GUI...")
    print("Console window will show debug output during processing.")
    print("=" * 60)
    main()
