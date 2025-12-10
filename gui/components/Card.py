"""
CardComponent
Reusable card container component
"""

import tkinter as tk
from gui.localization import t


class CardComponent:
    """Reusable card container component"""

    def __init__(self, parent, title, colors, spacing=20, padding=20):
        self.parent = parent
        self.title = title
        self.colors = colors
        self.spacing = spacing
        self.padding = padding
        self.card = None

    def render(self):
        """Render the card container"""
        card_container = tk.Frame(self.parent, bg=self.colors["bg"])
        card_container.pack(fill="x", pady=(0, self.spacing))

        self.card = tk.Frame(
            card_container, bg=self.colors["card"], relief="flat", highlightthickness=0
        )
        self.card.pack(fill="x")

        # Card header
        header = tk.Frame(self.card, bg=self.colors["card"])
        header.pack(fill="x", padx=self.padding, pady=(self.padding, 10))

        tk.Label(
            header,
            text=self.title,
            font=("SF Pro Text", 14, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).pack(anchor="w")

        return self.card
