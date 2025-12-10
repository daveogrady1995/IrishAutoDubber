"""
OutputSettingsCard
Output settings card component
"""

import tkinter as tk
from .Card import CardComponent
from gui.localization import t


class OutputSettingsCard:
    """Output settings card component"""

    def __init__(self, parent, colors, output_name_var, spacing=20, padding=20):
        self.parent = parent
        self.colors = colors
        self.output_name_var = output_name_var
        self.spacing = spacing
        self.padding = padding

    def render(self):
        """Render the output settings card"""
        # Create card
        card = CardComponent(self.parent, t("output_settings_title"), self.colors, self.spacing, self.padding)
        card_frame = card.render()

        # Output filename input
        output_inner = tk.Frame(card_frame, bg=self.colors["card"])
        output_inner.pack(fill="x", padx=self.padding, pady=(10, 0))

        tk.Label(
            output_inner,
            text=t("output_filename_label"),
            font=("SF Pro Text", 12, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).pack(anchor="w", pady=(0, 8))

        output_entry = tk.Entry(
            output_inner,
            textvariable=self.output_name_var,
            font=("SF Pro Text", 13),
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
        )
        output_entry.pack(fill="x", ipady=2, ipadx=2)

        return card_frame
