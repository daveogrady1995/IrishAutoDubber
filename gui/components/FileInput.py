"""
FileInputComponent
File input row component with label, display, and browse button
"""

import tkinter as tk
from .RoundedButton import RoundedButton
from gui.localization import t


class FileInputComponent:
    """File input row component with label, display, and browse button"""

    def __init__(
        self,
        parent,
        label,
        icon,
        var_key,
        filetypes,
        colors,
        file_display_var,
        browse_callback,
    ):
        self.parent = parent
        self.label = label
        self.icon = icon
        self.var_key = var_key
        self.filetypes = filetypes
        self.colors = colors
        self.file_display_var = file_display_var
        self.browse_callback = browse_callback

    def render(self):
        """Render the file input row"""
        row_frame = tk.Frame(self.parent, bg=self.colors["card"])
        row_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Label with icon
        label_frame = tk.Frame(row_frame, bg=self.colors["card"])
        label_frame.pack(fill="x", pady=(0, 8))

        tk.Label(
            label_frame,
            text=f"{self.icon}  {self.label}",
            font=("SF Pro Text", 12, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).pack(side="left")

        # File display and browse button container
        input_container = tk.Frame(row_frame, bg=self.colors["input_bg"], relief="flat")
        input_container.pack(fill="x")

        inner_container = tk.Frame(input_container, bg=self.colors["input_bg"])
        inner_container.pack(fill="x", padx=15, pady=12)

        # File name display
        file_label = tk.Label(
            inner_container,
            textvariable=self.file_display_var,
            font=("SF Pro Text", 12),
            bg=self.colors["input_bg"],
            fg=self.colors["text_light"],
            anchor="w",
        )
        file_label.pack(side="left", fill="x", expand=True)

        # Browse button
        browse_btn = RoundedButton(
            inner_container,
            text=t("browse_button"),
            command=lambda: self.browse_callback(self.var_key, self.filetypes),
            bg_color=self.colors["primary"],
            fg_color="white",
            hover_color=self.colors["primary_hover"],
            font=("SF Pro Text", 11, "bold"),
            width=100,
            height=36,
        )
        browse_btn.pack(side="right")

        return row_frame
