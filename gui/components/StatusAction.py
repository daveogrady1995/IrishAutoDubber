"""
StatusActionComponent
Status indicator and action button component
"""

import tkinter as tk
from .RoundedButton import RoundedButton
from gui.localization import t


class StatusActionComponent:
    """Status indicator and action button component"""

    def __init__(self, parent, colors, start_callback):
        self.parent = parent
        self.colors = colors
        self.start_callback = start_callback
        self.status_indicator = None
        self.status_label = None
        self.start_button = None

    def render(self):
        """Render the status and action section"""
        action_frame = tk.Frame(self.parent, bg=self.colors["bg"])
        action_frame.pack(fill="x", pady=(20, 0))

        # Status indicator
        status_container = tk.Frame(action_frame, bg=self.colors["card"], relief="flat")
        status_container.pack(fill="x", pady=(0, 15))

        status_inner = tk.Frame(status_container, bg=self.colors["card"])
        status_inner.pack(fill="x", padx=20, pady=15)

        self.status_indicator = tk.Label(
            status_inner,
            text="●",
            font=("SF Pro Text", 20),
            bg=self.colors["card"],
            fg=self.colors["text_light"],
        )
        self.status_indicator.pack(side="left", padx=(0, 10))

        self.status_label = tk.Label(
            status_inner,
            text=t("status_ready"),
            font=("SF Pro Text", 13),
            bg=self.colors["card"],
            fg=self.colors["text"],
        )
        self.status_label.pack(side="left")

        # Start button
        button_container = tk.Frame(action_frame, bg=self.colors["bg"])
        button_container.pack(fill="x")

        self.start_button = RoundedButton(
            button_container,
            text=t("start_button"),
            command=self.start_callback,
            bg_color=self.colors["primary"],
            fg_color="white",
            hover_color=self.colors["primary_hover"],
            font=("SF Pro Text", 15, "bold"),
            width=840,
            height=50,
        )
        self.start_button.pack()

        return action_frame
