"""
HeaderComponent
Header component with title and subtitle
"""

import tkinter as tk
from gui.localization import t


class HeaderComponent:
    """Header component with title and subtitle"""

    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.frame = None
        self.title_label = None
        self.subtitle_label = None

    def render(self, spacing=30):
        """Render the header component"""
        self.frame = tk.Frame(self.parent, bg=self.colors["bg"])
        self.frame.pack(fill="x", pady=(0, spacing))

        # Text content
        text_frame = tk.Frame(self.frame, bg=self.colors["bg"])
        text_frame.pack(fill="x")

        self.title_label = tk.Label(
            text_frame,
            text=t("header_title"),
            font=("SF Pro Display", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            text_frame,
            text=t("header_subtitle"),
            font=("SF Pro Text", 13),
            bg=self.colors["bg"],
            fg=self.colors["text_light"],
        )
        self.subtitle_label.pack(anchor="w", pady=(5, 0))

        return self.frame

    def update_text(self):
        """Update text when language changes"""
        if self.title_label:
            self.title_label.config(text=t("header_title"))
        if self.subtitle_label:
            self.subtitle_label.config(text=t("header_subtitle"))
