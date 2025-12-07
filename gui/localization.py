"""
Localization for Irish Auto-Dubbing Tool
Supports English and Irish (Gaeilge)
"""


class Localization:
    """Localization manager for multi-language support"""

    LANGUAGES = {
        "en": {
            # Window
            "window_title": "Abair - Irish Auto Dubbing",
            # Header
            "header_title": "Irish Auto Dubbing",
            "header_subtitle": "Dub your videos into Irish Gaelic with Abair.ie",
            # Upload Files Card
            "upload_files_title": "Upload Files",
            "video_file_label": "Video File",
            "video_file_icon": "🎬",
            "english_subtitles_label": "English Subtitles",
            "english_subtitles_icon": "🇬🇧",
            "irish_subtitles_label": "Irish Subtitles",
            "irish_subtitles_icon": "🇮🇪",
            "browse_button": "Browse",
            "no_file_selected": "No file selected",
            # Output Settings Card
            "output_settings_title": "Output Settings",
            "output_filename_label": "Output Filename",
            # Status & Action
            "status_ready": "Ready to start",
            "status_processing": "Processing - Please wait...",
            "status_complete": "Complete! Video ready",
            "status_failed": "Failed - See error message",
            "start_button": "Start Dubbing",
            "processing_button": "Processing...",
            # Dialogs
            "missing_file_title": "Missing File",
            "missing_file_message": "Please select a valid path for the {0}.",
            "process_failed_title": "Process Failed",
            "process_complete_title": "Process Complete",
            # File selection
            "select_file_title": "Select {0} file",
            "video_files": "Video Files",
            "srt_files": "SRT Files",
        },
        "ga": {
            # Window
            "window_title": "Abair - Uath-Dhubáil Ghaeilge",
            # Header
            "header_title": "Uath-Dhubáil Ghaeilge",
            "header_subtitle": "Dubáil do chuid físeán go Gaeilge le Abair.ie",
            # Upload Files Card
            "upload_files_title": "Uaslódáil Comhaid",
            "video_file_label": "Comhad Físe",
            "video_file_icon": "🎬",
            "english_subtitles_label": "Fotheidil Bhéarla",
            "english_subtitles_icon": "🇬🇧",
            "irish_subtitles_label": "Fotheidil Ghaeilge",
            "irish_subtitles_icon": "🇮🇪",
            "browse_button": "Brabhsáil",
            "no_file_selected": "Níl aon chomhad roghnaithe",
            # Output Settings Card
            "output_settings_title": "Socruithe Aschuir",
            "output_filename_label": "Ainm Comhaid Aschuir",
            # Status & Action
            "status_ready": "Réidh le tosú",
            "status_processing": "Á phróiseáil - Fan le do thoil...",
            "status_complete": "Críochnaithe! Físeán réidh",
            "status_failed": "Theip - Féach ar an earráid",
            "start_button": "Tosaigh an Dubáil",
            "processing_button": "Á phróiseáil...",
            # Dialogs
            "missing_file_title": "Comhad ar Iarraidh",
            "missing_file_message": "Roghnaigh cosán bailí le do thoil don {0}.",
            "process_failed_title": "Theip ar an bPróiseas",
            "process_complete_title": "Próiseas Críochnaithe",
            # File selection
            "select_file_title": "Roghnaigh comhad {0}",
            "video_files": "Comhaid Físe",
            "srt_files": "Comhaid SRT",
        },
    }

    def __init__(self, language="en"):
        """Initialize with default language"""
        self.current_language = language

    def set_language(self, language):
        """Change the current language"""
        if language in self.LANGUAGES:
            self.current_language = language
        else:
            raise ValueError(f"Language '{language}' not supported")

    def get(self, key, *args):
        """Get localized text for a key"""
        text = self.LANGUAGES.get(self.current_language, {}).get(key, key)
        if args:
            text = text.format(*args)
        return text

    def get_current_language(self):
        """Get current language code"""
        return self.current_language


# Global localization instance
_localization = Localization("en")


def get_localization():
    """Get the global localization instance"""
    return _localization


def set_language(language):
    """Set the global language"""
    _localization.set_language(language)


def t(key, *args):
    """Shorthand for translate - get localized text"""
    return _localization.get(key, *args)
