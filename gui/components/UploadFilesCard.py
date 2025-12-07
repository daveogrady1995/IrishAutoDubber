"""
UploadFilesCard
Upload files card component containing multiple file inputs
"""

from .Card import CardComponent
from .FileInput import FileInputComponent
from gui.localization import t


class UploadFilesCard:
    """Upload files card component containing multiple file inputs"""

    def __init__(self, parent, colors, paths, file_displays, browse_callback):
        self.parent = parent
        self.colors = colors
        self.paths = paths
        self.file_displays = file_displays
        self.browse_callback = browse_callback

    def render(self):
        """Render the upload files card with all file inputs in columns"""
        # Create card
        card = CardComponent(self.parent, t("upload_files_title"), self.colors)
        card_frame = card.render()

        # File input configurations
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
        import tkinter as tk

        columns_frame = tk.Frame(card_frame, bg=self.colors["card"])
        columns_frame.pack(fill="both", expand=True, pady=(15, 0))

        # Left column
        left_column = tk.Frame(columns_frame, bg=self.colors["card"])
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right column
        right_column = tk.Frame(columns_frame, bg=self.colors["card"])
        right_column.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Render file inputs in columns (video on left, subtitles on right)
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

        return card_frame
