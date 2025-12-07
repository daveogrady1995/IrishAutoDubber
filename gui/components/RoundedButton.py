"""
RoundedButton Component
Custom rounded button with Material Design styling
"""

import tkinter as tk


class RoundedButton(tk.Canvas):
    """Custom rounded button with Material Design styling"""

    def __init__(
        self,
        parent,
        text,
        command,
        bg_color,
        fg_color,
        hover_color,
        font=("SF Pro Text", 12, "bold"),
        width=120,
        height=40,
        **kwargs,
    ):
        tk.Canvas.__init__(
            self,
            parent,
            height=height,
            width=width,
            bg=parent.cget("bg"),
            highlightthickness=0,
            **kwargs,
        )

        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.height = height
        self.width = width
        self.is_disabled = False
        self.click_in_progress = False

        # Create rounded rectangle
        self.rect = self.create_rounded_rect(
            0, 0, width, height, radius=8, fill=bg_color
        )
        self.text_item = self.create_text(
            width / 2, height / 2, text=text, fill=fg_color, font=font
        )

        # Only bind to canvas level - prevents duplicate events
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self.config(cursor="hand2")

    def create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_press(self, event):
        # Record that we started a click on this button
        if not self.is_disabled and not self.click_in_progress:
            self.click_in_progress = True
            self.itemconfig(self.rect, fill=self.hover_color)
        return "break"  # Stop event propagation

    def _on_release(self, event):
        # Only execute if we had a press and release is within bounds
        if not self.is_disabled and self.click_in_progress:
            # Check if release is within button
            x, y = event.x, event.y
            if 0 <= x <= self.width and 0 <= y <= self.height:
                # Execute command ONCE
                if self.command:
                    try:
                        self.command()
                    except Exception as e:
                        print(f"Button command error: {e}")
            # Reset state
            self.click_in_progress = False
            self.itemconfig(self.rect, fill=self.bg_color)
        return "break"  # Stop event propagation

    def _on_enter(self, event):
        if not self.is_disabled:
            self.itemconfig(self.rect, fill=self.hover_color)

    def _on_leave(self, event):
        if not self.is_disabled:
            self.itemconfig(self.rect, fill=self.bg_color)

    def update_color(self, new_color):
        self.bg_color = new_color
        self.itemconfig(self.rect, fill=new_color)

    def update_text(self, new_text):
        self.text = new_text
        self.itemconfig(self.text_item, text=new_text)

    def disable(self):
        self.is_disabled = True
        self.config(cursor="arrow")

    def enable(self):
        self.is_disabled = False
        self.config(cursor="hand2")
