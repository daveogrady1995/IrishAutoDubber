"""
ImageComponent
Image display component with rounded corners
"""

import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw


class ImageComponent:
    """Reusable image component with rounded corners"""

    def __init__(
        self, parent, colors, image_names, max_width=400, max_height=150, radius=15
    ):
        self.parent = parent
        self.colors = colors
        self.image_names = (
            image_names if isinstance(image_names, list) else [image_names]
        )
        self.max_width = max_width
        self.max_height = max_height
        self.radius = radius
        self.photo = None

    def render(self):
        """Render the image component"""
        try:
            # Try to find the image
            image_path = None

            for img_name in self.image_names:
                # Go up three levels: components -> gui -> app
                potential_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    "images",
                    img_name,
                )
                if os.path.exists(potential_path):
                    image_path = potential_path
                    break

            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                # Resize image
                img.thumbnail(
                    (self.max_width, self.max_height), Image.Resampling.LANCZOS
                )

                # Create rounded corners
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle([(0, 0), img.size], radius=self.radius, fill=255)

                # Apply mask
                rounded_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
                rounded_img.paste(img, (0, 0))
                rounded_img.putalpha(mask)

                self.photo = ImageTk.PhotoImage(rounded_img)

                image_label = tk.Label(
                    self.parent, image=self.photo, bg=self.colors["bg"]
                )
                # Keep a reference to prevent garbage collection on macOS
                image_label.image = self.photo
                image_label.pack(side="left", pady=(0, 10))

                return image_label
        except Exception as e:
            print(f"Could not load image: {e}")
            return None
