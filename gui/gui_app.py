# gui_app.py - Modern UI for Irish Auto-Dubbing Tool

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os

# Use the shared wrapper module so GUI imports a single stable API.
from dubbing_core import run_dub


class RoundedButton(tk.Canvas):
    """Custom rounded button with Material Design styling"""
    def __init__(self, parent, text, command, bg_color, fg_color, hover_color, 
                 font=("SF Pro Text", 12, "bold"), width=120, height=40, **kwargs):
        tk.Canvas.__init__(self, parent, height=height, width=width, 
                          bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        
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
        self.rect = self.create_rounded_rect(0, 0, width, height, radius=8, fill=bg_color)
        self.text_item = self.create_text(width/2, height/2, text=text, 
                                         fill=fg_color, font=font)
        
        # Only bind to canvas level - prevents duplicate events
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self.config(cursor="hand2")
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
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


class DubbingApp:
    def __init__(self, master):
        self.master = master
        master.title("Abair - Irish Auto Dubbing")
        
        # Set window size and make it non-resizable for consistent look
        master.geometry("900x700")
        master.resizable(False, False)
        
        # Modern color scheme (light mode)
        self.colors = {
            'bg': '#F8F9FA',           # Light background
            'card': '#FFFFFF',          # White cards
            'primary': '#5B68F4',       # Bright indigo primary
            'primary_hover': '#4F5CE5', # Darker indigo
            'secondary': '#8B94FF',     # Light indigo secondary
            'success': '#10B981',       # Green
            'danger': '#EF4444',        # Red
            'text': '#1F2937',          # Dark gray text
            'text_light': '#6B7280',    # Light gray text
            'border': '#E5E7EB',        # Border gray
            'input_bg': '#F9FAFB',      # Input background
        }
        
        # Configure master background
        master.configure(bg=self.colors['bg'])
        
        # --- Variables to store selected file paths ---
        self.paths = {
            "video": tk.StringVar(),
            "eng_srt": tk.StringVar(),
            "gael_srt": tk.StringVar(),
        }
        # Variable for the output filename (default name is set here)
        self.output_name = tk.StringVar(value="dubbed_output.mp4")
        
        # File display names (shortened paths)
        self.file_displays = {
            "video": tk.StringVar(value="No file selected"),
            "eng_srt": tk.StringVar(value="No file selected"),
            "gael_srt": tk.StringVar(value="No file selected"),
        }

        # --- Create all the visual elements (widgets) ---
        self.create_widgets()

    def create_widgets(self):
        # Main container with padding
        main_container = tk.Frame(self.master, bg=self.colors['bg'])
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = tk.Label(
            header_frame,
            text="Irish Auto Dubbing",
            font=("SF Pro Display", 28, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            header_frame,
            text="Dub your videos into Irish Gaelic with Abair.ie",
            font=("SF Pro Text", 13),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # 1. Input Files Card
        files_card = self.create_card(main_container, "Upload Files")
        
        files_to_select = [
            ("Video File", "video", [("Video Files", "*.mp4 *.mov *.avi")], "🎬"),
            ("English Subtitles", "eng_srt", [("SRT Files", "*.srt")], "🇬🇧"),
            ("Irish Subtitles", "gael_srt", [("SRT Files", "*.srt")], "🇮🇪"),
        ]

        for i, (label_text, var_key, filetypes, icon) in enumerate(files_to_select):
            self.create_file_input(files_card, label_text, var_key, filetypes, icon, i)
        
        # 2. Output Configuration Card
        output_card = self.create_card(main_container, "Output Settings")
        
        output_inner = tk.Frame(output_card, bg=self.colors['card'])
        output_inner.pack(fill="x", padx=20, pady=(10, 20))
        
        tk.Label(
            output_inner,
            text="Output Filename",
            font=("SF Pro Text", 12, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor="w", pady=(0, 8))
        
        output_entry = tk.Entry(
            output_inner,
            textvariable=self.output_name,
            font=("SF Pro Text", 13),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        output_entry.pack(fill="x", ipady=10, ipadx=12)

        # 3. Status and Action Section
        action_frame = tk.Frame(main_container, bg=self.colors['bg'])
        action_frame.pack(fill="x", pady=(20, 0))
        
        # Status indicator
        status_container = tk.Frame(action_frame, bg=self.colors['card'], relief="flat")
        status_container.pack(fill="x", pady=(0, 15))
        
        status_inner = tk.Frame(status_container, bg=self.colors['card'])
        status_inner.pack(fill="x", padx=20, pady=15)
        
        self.status_indicator = tk.Label(
            status_inner,
            text="●",
            font=("SF Pro Text", 20),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        self.status_indicator.pack(side="left", padx=(0, 10))
        
        self.status_label = tk.Label(
            status_inner,
            text="Ready to start",
            font=("SF Pro Text", 13),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        self.status_label.pack(side="left")
        
        # Start button - Using custom rounded button
        button_container = tk.Frame(action_frame, bg=self.colors['bg'])
        button_container.pack(fill="x")
        
        self.start_button = RoundedButton(
            button_container,
            text="Start Dubbing",
            command=self.start_dubbing_thread,
            bg_color=self.colors['primary'],
            fg_color="white",
            hover_color=self.colors['primary_hover'],
            font=("SF Pro Text", 15, "bold"),
            width=840,  # Full width minus padding
            height=50
        )
        self.start_button.pack()
    
    def create_card(self, parent, title):
        """Create a modern card container"""
        card_container = tk.Frame(parent, bg=self.colors['bg'])
        card_container.pack(fill="x", pady=(0, 20))
        
        card = tk.Frame(card_container, bg=self.colors['card'], relief="flat", highlightthickness=0)
        card.pack(fill="x")
        
        # Card header
        header = tk.Frame(card, bg=self.colors['card'])
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(
            header,
            text=title,
            font=("SF Pro Text", 16, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor="w")
        
        return card
    
    def create_file_input(self, parent, label, var_key, filetypes, icon, index):
        """Create a modern file input row"""
        row_frame = tk.Frame(parent, bg=self.colors['card'])
        row_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Label with icon
        label_frame = tk.Frame(row_frame, bg=self.colors['card'])
        label_frame.pack(fill="x", pady=(0, 8))
        
        tk.Label(
            label_frame,
            text=f"{icon}  {label}",
            font=("SF Pro Text", 12, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(side="left")
        
        # File display and browse button container
        input_container = tk.Frame(row_frame, bg=self.colors['input_bg'], relief="flat")
        input_container.pack(fill="x")
        
        inner_container = tk.Frame(input_container, bg=self.colors['input_bg'])
        inner_container.pack(fill="x", padx=15, pady=12)
        
        # File name display
        file_label = tk.Label(
            inner_container,
            textvariable=self.file_displays[var_key],
            font=("SF Pro Text", 12),
            bg=self.colors['input_bg'],
            fg=self.colors['text_light'],
            anchor="w"
        )
        file_label.pack(side="left", fill="x", expand=True)
        
        # Browse button - Using custom rounded button
        browse_btn = RoundedButton(
            inner_container,
            text="Browse",
            command=lambda: self.browse_file(var_key, filetypes),
            bg_color=self.colors['primary'],
            fg_color="white",
            hover_color=self.colors['primary_hover'],
            font=("SF Pro Text", 11, "bold"),
            width=100,
            height=36
        )
        browse_btn.pack(side="right")

    def browse_file(self, var_key, filetypes):
        filepath = filedialog.askopenfilename(
            title=f"Select {var_key.replace('_', ' ')} file", filetypes=filetypes
        )
        if filepath:
            self.paths[var_key].set(filepath)
            # Update display with shortened filename
            filename = os.path.basename(filepath)
            if len(filename) > 50:
                filename = filename[:47] + "..."
            self.file_displays[var_key].set(filename)

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
        self.start_button.disable()
        self.start_button.update_text("Processing...")
        self.start_button.update_color(self.colors['text_light'])
        self.status_label.config(text="Processing - Please wait...")
        self.status_indicator.config(fg="#F59E0B")  # Orange

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
        self.start_button.update_text("Start Dubbing")
        self.start_button.update_color(self.colors['primary'])
        self.start_button.config(cursor="hand2")

        # Check for error prefix or red color
        if color == "red" or message.startswith("ERROR:"):
            messagebox.showerror("Process Failed", message)
            self.status_label.config(text="Failed - See error message")
            self.status_indicator.config(fg=self.colors['danger'])
        else:
            messagebox.showinfo("Process Complete", message)
            self.status_label.config(text="Complete! Video ready")
            self.status_indicator.config(fg=self.colors['success'])


if __name__ == "__main__":
    root = tk.Tk()
    app = DubbingApp(root)
    root.mainloop()


def main():
    """Entry point used by `run_gui.py` and by a frozen EXE."""
    root = tk.Tk()
    app = DubbingApp(root)
    root.mainloop()
