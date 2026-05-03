"""
UploadFilesCard
Upload files card component containing multiple file inputs
"""

import tkinter as tk

from .Card import CardComponent
from .FileInput import FileInputComponent
from gui.localization import t


class UploadFilesCard:
    """Upload files card component containing multiple file inputs"""

    def __init__(
        self,
        parent,
        colors,
        paths,
        file_displays,
        browse_callback,
        auto_dub_var=None,
        spacing=20,
        padding=20,
    ):
        self.parent = parent
        self.colors = colors
        self.paths = paths
        self.file_displays = file_displays
        self.browse_callback = browse_callback
        self.auto_dub_var = auto_dub_var or tk.BooleanVar(value=False)
        self.spacing = spacing
        self.padding = padding
        # Keep references to SRT widgets so we can toggle them
        self._srt_frame = None

    def _on_auto_dub_toggle(self):
        """Show/hide the SRT file pickers based on the checkbox state."""
        if self._srt_frame is None:
            return
        if self.auto_dub_var.get():
            self._srt_frame.pack_forget()
        else:
            self._srt_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

    def render(self):
        """Render the upload files card with all file inputs in columns"""
        # Create card
        card = CardComponent(
            self.parent,
            t("upload_files_title"),
            self.colors,
            self.spacing,
            self.padding,
        )
        card_frame = card.render()

        # --- Auto-dub checkbox ---
        checkbox_frame = tk.Frame(card_frame, bg=self.colors["card"])
        checkbox_frame.pack(fill="x", pady=(4, 2))

        auto_dub_cb = tk.Checkbutton(
            checkbox_frame,
            text=t("auto_dub_label"),
            variable=self.auto_dub_var,
            command=self._on_auto_dub_toggle,
            bg=self.colors["card"],
            fg=self.colors["primary"],
            activebackground=self.colors["card"],
            activeforeground=self.colors["primary"],
            selectcolor=self.colors["card"],
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )
        auto_dub_cb.pack(side="left")

        auto_dub_desc = tk.Label(
            checkbox_frame,
            text=t("auto_dub_description"),
            bg=self.colors["card"],
            fg=self.colors["text_light"],
            font=("Segoe UI", 8),
        )
        auto_dub_desc.pack(side="left", padx=(6, 0))

        # --- File input configurations ---
        files_config = [
            {
                "label": t("video_file_label"),
                "var_key": "video",
                "filetypes": [(t("video_files"), "*.mp4 *.mov *.avi")],
                "icon": t("video_file_icon"),
            },
            {
                "label": t("english_subtitles_label"),
                "var_key": "eng_srt",
                "filetypes": [(t("srt_files"), "*.srt")],
                "icon": t("english_subtitles_icon"),
            },
            {
                "label": t("irish_subtitles_label"),
                "var_key": "gael_srt",
                "filetypes": [(t("srt_files"), "*.srt")],
                "icon": t("irish_subtitles_icon"),
            },
        ]

        # Create a two-column layout
        columns_frame = tk.Frame(card_frame, bg=self.colors["card"])
        columns_frame.pack(fill="both", expand=True, pady=(8, 0))

        # Left column — always visible (video)
        left_column = tk.Frame(columns_frame, bg=self.colors["card"])
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right column — hidden in auto-dub mode
        right_column = tk.Frame(columns_frame, bg=self.colors["card"])
        right_column.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self._srt_frame = right_column

        # Video file in left column
        file_input_video = FileInputComponent(
            left_column,
            files_config[0]["label"],
            files_config[0]["icon"],
            files_config[0]["var_key"],
            files_config[0]["filetypes"],
            self.colors,
            self.file_displays[files_config[0]["var_key"]],
            self.browse_callback,
        )
        file_input_video.render()

        # English subtitles in right column (top)
        file_input_eng = FileInputComponent(
            right_column,
            files_config[1]["label"],
            files_config[1]["icon"],
            files_config[1]["var_key"],
            files_config[1]["filetypes"],
            self.colors,
            self.file_displays[files_config[1]["var_key"]],
            self.browse_callback,
        )
        file_input_eng.render()

        # Irish subtitles in right column (bottom)
        file_input_gael = FileInputComponent(
            right_column,
            files_config[2]["label"],
            files_config[2]["icon"],
            files_config[2]["var_key"],
            files_config[2]["filetypes"],
            self.colors,
            self.file_displays[files_config[2]["var_key"]],
            self.browse_callback,
        )
        file_input_gael.render()

        # Apply initial state if auto-dub is already checked (e.g. after language switch)
        if self.auto_dub_var.get():
            self._on_auto_dub_toggle()

        return card_frame
