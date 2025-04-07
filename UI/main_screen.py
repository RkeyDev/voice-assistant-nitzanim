import tkinter as tk
from typing import Callable
from tkinter import ttk, PhotoImage
import threading

WINDOW_SIZE = "800x500"

class MainScreen:
    def __init__(self, run_app_func: Callable) -> None:
        self.run_app_func = run_app_func
        self.root = None
        self.mic_button = None
        self.mic_idle_image = None
        self.mic_listening_image = None
        self.is_listening = False
        self.status_label = None

    def run_app(self):
        if self.is_listening:
            self.is_listening = False
            self.mic_button.config(image=self.mic_idle_image)
            self.root.update_idletasks()
            return
        self.is_listening = True
        self.mic_button.config(image=self.mic_listening_image)
        self.root.update_idletasks()

        def active_voice_assistant():
            self.run_app_func()
            self.mic_button.config(image=self.mic_idle_image)

        thread = threading.Thread(target=active_voice_assistant)
        thread.setDaemon(True)
        thread.start()

    def update_status(self, text: str) -> None:
        if self.status_label:
            self.status_label.config(text=text)

    def start_window(self) -> None:
        self.root = tk.Tk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title("Python Voice Assistant")

        background_color = "#f0f4f8"
        header_color = "#2c3e50"
        accent_color = "#3498db"

        self.root.configure(bg=background_color)

        header = tk.Label(self.root, text="Python Voice Assistant", 
                          bg=header_color, fg="white", 
                          font=("Helvetica", 24, "bold"), padx=20, pady=10)
        header.pack(fill=tk.X, side=tk.TOP)

        self.mic_idle_image = PhotoImage(file="assets/mic_idle.png")
        self.mic_listening_image = PhotoImage(file="assets/mic_listening.png")
        
        center_frame = tk.Frame(self.root, bg=background_color)
        center_frame.pack(expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Accent.TButton",
                        background=accent_color,
                        foreground="white",
                        font=("Helvetica", 16, "bold"),
                        borderwidth=0)
        style.map("Accent.TButton",
                  background=[("active", "#2980b9")])

        self.mic_button = ttk.Button(center_frame, image=self.mic_idle_image,
                                     command=self.run_app, style="Accent.TButton")
        self.mic_button.pack(pady=20)

        self.status_label = tk.Label(center_frame, text="Click the mic to start",
                                     bg=background_color, fg=header_color,
                                     font=("Helvetica", 14))
        self.status_label.pack(pady=10)

        self.root.mainloop()
