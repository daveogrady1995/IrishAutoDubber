"""
CardComponent
Reusable card container component
"""

import tkinter as tk
from gui.localization import t


class CardComponent:
    """Reusable card container component"""

    def __init__(self, parent, title, colors):
        self.parent = parent
        self.title = title
        self.colors = colors
        self.card = None

    def render(self):
        """Render the card container"""
        card_container = tk.Frame(self.parent, bg=self.colors["bg"])
        card_container.pack(fill="x", pady=(0, 20))

        self.card = tk.Frame(
            card_container, bg=self.colors["card"], relief="flat", highlightthickness=0
        )
        self.card.pack(fill="x")

        # Card header
        header = tk.Frame(self.card, bg=self.colors["card"])
        header.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(
            header,
            text=self.title,
            font=("SF Pro Text", 16, "bold"),
            bg=self.colors["card"],
            fg=self.colors["text"],
        ).pack(anchor="w")

        return self.card
