"""
Progress observer for tracking dubbing progress
"""

from abc import ABC, abstractmethod
from typing import Optional


class ProgressObserver(ABC):
    """Abstract base class for progress observers"""

    @abstractmethod
    def on_progress(
        self, current: int, total: int, stage: str, message: Optional[str] = None
    ):
        """
        Called when progress is updated

        Args:
            current: Current progress value
            total: Total progress value
            stage: Current stage name (e.g., "Parsing", "Dubbing", "Mixing")
            message: Optional detailed message
        """
        pass

    @abstractmethod
    def on_stage_start(self, stage: str):
        """Called when a new stage starts"""
        pass

    @abstractmethod
    def on_stage_complete(self, stage: str):
        """Called when a stage completes"""
        pass

    @abstractmethod
    def on_error(self, error: str):
        """Called when an error occurs"""
        pass

    @abstractmethod
    def on_complete(self, output_path: str):
        """Called when entire process completes successfully"""
        pass


class ConsoleProgressObserver(ProgressObserver):
    """Console-based progress observer using print statements"""

    def on_progress(
        self, current: int, total: int, stage: str, message: Optional[str] = None
    ):
        """Print progress bar to console"""
        percent = int(100 * current / total) if total > 0 else 0
        filled = int(40 * current / total) if total > 0 else 0
        bar = "█" * filled + "-" * (40 - filled)
        msg = f" {message}" if message else ""
        print(f"\r{stage}: |{bar}| {percent}%{msg}", end="", flush=True)
        if current == total:
            print()  # New line when complete

    def on_stage_start(self, stage: str):
        """Print stage start message"""
        print(f"\n{stage}...")

    def on_stage_complete(self, stage: str):
        """Print stage completion message"""
        print(f"✓ {stage} complete")

    def on_error(self, error: str):
        """Print error message"""
        print(f"\n✗ Error: {error}")

    def on_complete(self, output_path: str):
        """Print completion message"""
        print(f"\n✓ DONE! Output: {output_path}")


class NoOpProgressObserver(ProgressObserver):
    """No-operation progress observer that does nothing"""

    def on_progress(
        self, current: int, total: int, stage: str, message: Optional[str] = None
    ):
        pass

    def on_stage_start(self, stage: str):
        pass

    def on_stage_complete(self, stage: str):
        pass

    def on_error(self, error: str):
        pass

    def on_complete(self, output_path: str):
        pass
