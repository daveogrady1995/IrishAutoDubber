# gui_app.py - copied from `source/gui_app.py` and adjusted to be the real
# `gui.gui_app` entrypoint. It imports the shared `dubbing_core` wrapper.

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

# Use the shared wrapper module so GUI imports a single stable API.
from dubbing_core import run_dub

# ... rest of your code ...


class DubbingApp:
    def __init__(self, master):
        self.master = master
        master.title("Abair Dubbing Tool")

        # --- Variables to store selected file paths ---
        self.paths = {
            "video": tk.StringVar(),
            "eng_srt": tk.StringVar(),
            "gael_srt": tk.StringVar(),
        }
        # Variable for the output filename (default name is set here)
        self.output_name = tk.StringVar(value="dubbed_output.mp4")

        # --- Create all the visual elements (widgets) ---
        self.create_widgets()

    def create_widgets(self):
        # 1. Input Files Section
        file_frame = tk.LabelFrame(self.master, text="📂 Input Files", padx=10, pady=10)
        file_frame.pack(padx=10, pady=10, fill="x")

        files_to_select = [
            ("Input Video (.mp4):", "video", [("Video Files", "*.mp4")]),
            ("English Subtitles (.srt):", "eng_srt", [("SRT Subtitles", "*.srt")]),
            ("Irish Subtitles (.srt):", "gael_srt", [("SRT Subtitles", "*.srt")]),
        ]

        for i, (label_text, var_key, filetypes) in enumerate(files_to_select):
            tk.Label(file_frame, text=label_text).grid(
                row=i, column=0, sticky="w", pady=2
            )
            # Use a lambda for the command to correctly pass arguments
            entry = tk.Entry(
                file_frame, textvariable=self.paths[var_key], width=50, state="readonly"
            )
            entry.grid(row=i, column=1, padx=5)
            browse_cmd = lambda key=var_key, ftypes=filetypes: self.browse_file(
                key, ftypes
            )
            tk.Button(file_frame, text="Browse", command=browse_cmd).grid(
                row=i, column=2
            )

        # 2. Output Configuration Section
        output_frame = tk.LabelFrame(
            self.master, text="⚙️ Output Configuration", padx=10, pady=10
        )
        output_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(output_frame, text="Output Filename:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        tk.Entry(output_frame, textvariable=self.output_name, width=50).grid(
            row=0, column=1, padx=5
        )

        # 3. Control and Status Section
        control_frame = tk.Frame(self.master, padx=10, pady=5)
        control_frame.pack(fill="x")
        self.status_label = tk.Label(control_frame, text="Status: Ready", fg="blue")
        self.status_label.pack(side="left", padx=10)

        self.start_button = tk.Button(
            control_frame,
            text="🚀 Start Dubbing Process",
            command=self.start_dubbing_thread,
            bg="green",
            fg="white",
            font=("Helvetica", 10, "bold"),
        )
        self.start_button.pack(side="right", pady=5)

    def browse_file(self, var_key, filetypes):
        filepath = filedialog.askopenfilename(
            title=f"Select {var_key.replace('_', ' ')} file", filetypes=filetypes
        )
        if filepath:
            self.paths[var_key].set(filepath)

    def start_dubbing_thread(self):
        # 1. Validation Check: Make sure the user selected all three files
        required_files = ["video", "eng_srt", "gael_srt"]
        for key in required_files:
            if not self.paths[key].get() or not os.path.exists(self.paths[key].get()):
                messagebox.showerror(
                    "Missing File",
                    f"Please select a valid path for the {key.replace('_', ' ')}.",
                )
                return

        # 2. Disable button and update status
        self.start_button.config(state=tk.DISABLED, text="Processing...")
        self.status_label.config(
            text="Status: Working (Do not close this app)", fg="orange"
        )

        # 3. Start the process in a new thread.
        process_thread = threading.Thread(target=self.run_process_in_thread)
        process_thread.start()

    def run_process_in_thread(self):
        """This function runs your main script's heavy lifting (now app_main.py)."""
        try:
            # Gather the selected paths and output name
            args = (
                self.paths["video"].get(),
                self.paths["eng_srt"].get(),
                self.paths["gael_srt"].get(),
                self.output_name.get(),
            )

            # EXECUTE YOUR CORE DUBBING SCRIPT (via shared `dubbing_core` wrapper)
            result_message = run_dub(*args)

            self.master.after(0, lambda: self.finish_process(result_message, "green"))

        except Exception as e:
            error_msg = f"ERROR: An unexpected error occurred: {e}"  # Prefix with ERROR for explicit handling
            print(error_msg)
            self.master.after(0, lambda: self.finish_process(error_msg, "red"))

    def finish_process(self, message, color):
        self.start_button.config(state=tk.NORMAL, text="🚀 Start Dubbing Process")

        # Check for error prefix or red color
        if color == "red" or message.startswith("ERROR:"):
            messagebox.showerror("Process Failed", message)
            self.status_label.config(text="Status: FAILED.", fg="red")
        else:
            messagebox.showinfo("Process Complete", message)
            self.status_label.config(text="Status: Complete!", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = DubbingApp(root)
    root.mainloop()


def main():
    """Entry point used by `run_gui.py` and by a frozen EXE."""
    root = tk.Tk()
    app = DubbingApp(root)
    root.mainloop()
