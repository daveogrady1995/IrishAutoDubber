# gui_app.py - Modern UI for Irish Auto-Dubbing Tool (React-like Components)

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

# Use the shared wrapper module so GUI imports a single stable API.
from dubbing_core import run_dub

# Import all components from the components module
from gui.components import (
    HeaderComponent,
    UploadFilesCard,
    OutputSettingsCard,
    StatusActionComponent,
    ImageComponent,
)

# Import localization
from gui.localization import t, set_language, get_localization
from gui.helpers import create_language_selector
from gui.window_utils import setup_responsive_window, apply_macos_fix

# ============================================================================
# MAIN APP COMPONENT (Container)
# ============================================================================


class DubbingApp:
    """Main application container - React-like root component"""

    def __init__(self, master):
        self.master = master
        master.title(t("window_title"))

        # Responsive window sizing based on screen size
        self.window_scale = setup_responsive_window(master)

        # Modern color scheme (light mode)
        self.colors = {
            "bg": "#F8F9FA",  # Light background
            "card": "#FFFFFF",  # White cards
            "primary": "#5B68F4",  # Bright indigo primary
            "primary_hover": "#4F5CE5",  # Darker indigo
            "secondary": "#8B94FF",  # Light indigo secondary
            "success": "#10B981",  # Green
            "danger": "#EF4444",  # Red
            "text": "#1F2937",  # Dark gray text
            "text_light": "#6B7280",  # Light gray text
            "border": "#E5E7EB",  # Border gray
            "input_bg": "#F9FAFB",  # Input background
        }

        # Configure master background
        master.configure(bg=self.colors["bg"])

        # --- Application State (React-like state) ---
        self.paths = {
            "video": tk.StringVar(),
            "eng_srt": tk.StringVar(),
            "gael_srt": tk.StringVar(),
        }

        self.output_name = tk.StringVar(value="dubbed_output.mp4")

        self.file_displays = {
            "video": tk.StringVar(value=t("no_file_selected")),
            "eng_srt": tk.StringVar(value=t("no_file_selected")),
            "gael_srt": tk.StringVar(value=t("no_file_selected")),
        }

        # Component references
        self.image_component = None
        self.header_component = None
        self.upload_files_component = None
        self.output_settings_component = None
        self.status_action_component = None

        # Render the app
        self.create_widgets()
        
        # macOS Sonoma fix: Slightly move window to refresh mouse responsiveness
        # This fixes a known tkinter bug on macOS 14+ where buttons ignore clicks
        self.master.after(100, lambda: apply_macos_fix(self.master))

    def create_widgets(self):
        """Render method - composes all child components"""
        # Main container with responsive padding
        padding = self.window_scale["padding"]
        main_container = tk.Frame(self.master, bg=self.colors["bg"])
        main_container.pack(fill="both", expand=True, padx=padding, pady=padding)

        # Top row: Image (left) and Language Selector (right)
        # Reduce vertical spacing on smaller screens
        top_pady = (0, 15) if self.window_scale["height"] < 900 else (0, 20)
        top_row = tk.Frame(main_container, bg=self.colors["bg"])
        top_row.pack(fill="x", pady=top_pady)

        # Render Image Component (left side of top row)
        image_container = tk.Frame(top_row, bg=self.colors["bg"])
        image_container.pack(side="left", fill="both", expand=True)

        # Scale image based on window size
        image_scale = self.window_scale.get("image_scale", 1.0)
        self.image_component = ImageComponent(
            image_container,
            self.colors,
            ["image1.png"],
            max_width=int(150 * image_scale),
            max_height=int(100 * image_scale),
        )
        self.image_component.render()

        # Language Selector (right side of top row)
        lang_selector = create_language_selector(
            top_row, self.colors, self.change_language
        )
        lang_selector.pack(side="right")

        # Render Header Component with responsive spacing
        header_spacing = self.window_scale.get("component_spacing", 20)
        self.header_component = HeaderComponent(main_container, self.colors)
        self.header_component.render(spacing=header_spacing)

        # Render Upload Files Card Component with responsive spacing
        card_spacing = self.window_scale.get("card_spacing", 15)
        card_padding = self.window_scale.get("card_padding", 15)
        self.upload_files_component = UploadFilesCard(
            main_container,
            self.colors,
            self.paths,
            self.file_displays,
            self.browse_file,
            spacing=card_spacing,
            padding=card_padding,
        )
        self.upload_files_component.render()

        # Render Output Settings Card Component with responsive spacing
        self.output_settings_component = OutputSettingsCard(
            main_container, self.colors, self.output_name,
            spacing=card_spacing, padding=card_padding
        )
        self.output_settings_component.render()

        # Render Status & Action Component
        self.status_action_component = StatusActionComponent(
            main_container, self.colors, self.start_dubbing_thread
        )
        self.status_action_component.render()

    def change_language(self, lang_code):
        """Handle language change"""
        set_language(lang_code)

        # Update window title
        self.master.title(t("window_title"))

        # Update header
        if self.header_component:
            self.header_component.update_text()

        # Rebuild the UI to reflect language changes
        # Clear and recreate widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Reset component references
        self.image_component = None
        self.header_component = None
        self.upload_files_component = None
        self.output_settings_component = None
        self.status_action_component = None

        # Update file display strings
        for key in self.file_displays:
            current_val = self.file_displays[key].get()
            if current_val in ["No file selected", "Níl aon chomhad roghnaithe"]:
                self.file_displays[key].set(t("no_file_selected"))

        # Recreate widgets
        self.create_widgets()

    def browse_file(self, var_key, filetypes):
        """Event handler for file browsing"""
        filepath = filedialog.askopenfilename(
            title=t("select_file_title", var_key.replace("_", " ")), filetypes=filetypes
        )
        if filepath:
            self.paths[var_key].set(filepath)
            # Update display with shortened filename
            filename = os.path.basename(filepath)
            if len(filename) > 50:
                filename = filename[:47] + "..."
            self.file_displays[var_key].set(filename)

    def start_dubbing_thread(self):
        """Event handler for starting dubbing process"""
        # 1. Validation Check
        required_files = ["video", "eng_srt", "gael_srt"]
        for key in required_files:
            if not self.paths[key].get() or not os.path.exists(self.paths[key].get()):
                messagebox.showerror(
                    t("missing_file_title"),
                    t("missing_file_message", key.replace("_", " ")),
                )
                return

        # 2. Update UI state
        self.status_action_component.start_button.disable()
        self.status_action_component.start_button.update_text(t("processing_button"))
        self.status_action_component.start_button.update_color(
            self.colors["text_light"]
        )
        self.status_action_component.status_label.config(text=t("status_processing"))
        self.status_action_component.status_indicator.config(fg="#F59E0B")  # Orange

        # 3. Start the process in a new thread
        process_thread = threading.Thread(target=self.run_process_in_thread)
        process_thread.start()

    def run_process_in_thread(self):
        """Background process execution"""
        try:
            # Gather the selected paths and output name
            args = (
                self.paths["video"].get(),
                self.paths["eng_srt"].get(),
                self.paths["gael_srt"].get(),
                self.output_name.get(),
            )

            # Execute core dubbing script
            result_message = run_dub(*args)

            self.master.after(0, lambda: self.finish_process(result_message, "green"))

        except Exception as e:
            error_msg = f"ERROR: An unexpected error occurred: {e}"
            print(error_msg)
            self.master.after(0, lambda: self.finish_process(error_msg, "red"))

    def finish_process(self, message, color):
        """Process completion handler - updates UI state"""
        self.status_action_component.start_button.update_text(t("start_button"))
        self.status_action_component.start_button.update_color(self.colors["primary"])
        self.status_action_component.start_button.enable()

        # Check for error
        if color == "red" or message.startswith("ERROR:"):
            messagebox.showerror(t("process_failed_title"), message)
            self.status_action_component.status_label.config(text=t("status_failed"))
            self.status_action_component.status_indicator.config(
                fg=self.colors["danger"]
            )
        else:
            messagebox.showinfo(t("process_complete_title"), message)
            self.status_action_component.status_label.config(text=t("status_complete"))
            self.status_action_component.status_indicator.config(
                fg=self.colors["success"]
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = DubbingApp(root)
    root.mainloop()


def main():
    """Entry point used by `run_gui.py` and by a frozen EXE."""
    root = tk.Tk()
    app = DubbingApp(root)
    root.mainloop()
