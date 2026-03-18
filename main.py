import os
import threading
import customtkinter as ctk
from tkinter import messagebox
import yt_dlp

# --- UI Configuration ---
ctk.set_appearance_mode("dark")
BG_COLOR = "#000000"
ACCENT_COLOR = "#39FF14"  # Neon Green

class RightsModal(ctk.CTkToplevel):
    def __init__(self, parent, on_proceed):
        super().__init__(parent)
        self.title("Rights Confirmation")
        self.geometry("400x200")
        self.configure(fg_color=BG_COLOR)
        self.on_proceed = on_proceed
        self.result = False

        # Ensure modal behavior
        self.transient(parent)
        self.grab_set()

        label = ctk.CTkLabel(self, text="Legal Affirmation", font=("Orbitron", 18, "bold"), text_color=ACCENT_COLOR)
        label.pack(pady=10)

        msg = ctk.CTkLabel(self, text="By clicking 'Proceed,' I certify that I own the rights\nto this content or have explicit permission to\ndownload it for legal use.", 
                           wraplength=350, text_color="white")
        msg.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray", command=self.destroy).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Proceed", fg_color=ACCENT_COLOR, text_color="black", hover_color="#32CD32", 
                      command=self._confirm).pack(side="left", padx=10)

    def _confirm(self):
        self.on_proceed()
        self.destroy()

class CyberDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CYBER-DL // NEON G")
        self.geometry("600x450")
        self.configure(fg_color=BG_COLOR)

        # Header
        self.header = ctk.CTkLabel(self, text="MEDIA CONVERTER v1.0", font=("Orbitron", 24, "bold"), text_color=ACCENT_COLOR)
        self.header.pack(pady=20)

        # Input
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste YouTube/Spotify Link Here...", width=450, 
                                       border_color=ACCENT_COLOR, fg_color="#1A1A1A")
        self.url_entry.pack(pady=10)

        # Format Selection
        self.format_var = ctk.StringVar(value="mp3")
        self.format_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.format_frame.pack(pady=10)
        
        ctk.CTkRadioButton(self.format_frame, text="MP3 (320kbps Audio)", variable=self.format_var, value="mp3", 
                           border_color=ACCENT_COLOR, fg_color=ACCENT_COLOR, text_color="white").pack(side="left", padx=20)
        ctk.CTkRadioButton(self.format_frame, text="MP4 (1080p+ Video)", variable=self.format_var, value="mp4", 
                           border_color=ACCENT_COLOR, fg_color=ACCENT_COLOR, text_color="white").pack(side="left", padx=20)

        # Status & Progress
        self.status_label = ctk.CTkLabel(self, text="IDLE", text_color=ACCENT_COLOR)
        self.status_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400, progress_color=ACCENT_COLOR, fg_color="#1A1A1A")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Action Button
        self.dl_button = ctk.CTkButton(self, text="INITIATE DOWNLOAD", font=("Orbitron", 14, "bold"), 
                                       fg_color=ACCENT_COLOR, text_color="black", hover_color="#32CD32",
                                       height=45, command=self.check_rights)
        self.dl_button.pack(pady=20)

    def check_rights(self):
        if not self.url_entry.get().strip():
            messagebox.showerror("Error", "Please provide a valid URL.")
            return
        RightsModal(self, self.start_download_thread)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            self.progress_bar.set(float(p)/100)
            self.status_label.configure(text=f"DOWNLOADING: {p}%")
        elif d['status'] == 'finished':
            self.status_label.configure(text="CONVERTING...")

    def start_download_thread(self):
        thread = threading.Thread(target=self.download_media, daemon=True)
        thread.start()

    def download_media(self):
        url = self.url_entry.get()
        fmt = self.format_var.get()
        self.status_label.configure(text="AUTHENTICATING RIGHTS...")
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if fmt == 'mp4' else 'bestaudio/best',
            'progress_hooks': [self.progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }] if fmt == 'mp3' else [],
            'outtmpl': '%(title)s.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.configure(text="SUCCESS")
            self.progress_bar.set(1)
        except Exception as e:
            self.status_label.configure(text="ERROR")
            messagebox.showerror("Download Error", str(e))

if __name__ == "__main__":
    app = CyberDownloader()
    app.mainloop()
