import tkinter as tk
from typing import Callable
from tkinter import ttk
from tkinter import Tk
import threading
import sys

WINDOW_SIZE:str = "500x300"

class MainScreen:
    def __init__(self,run_app_func:Callable) -> None: 
        self.run_app_func = run_app_func


    def run_app(self):
        thread = threading.Thread(target=self.run_app_func)
        thread.setDaemon(True)
        thread.start()

    def start_window(self) -> None:
        
        root = Tk() #Create the window object
        frm = ttk.Frame(root, padding=10) #Setup the window
        frm.grid()
        root.geometry(WINDOW_SIZE)
        root.title("Python voice assistant")
        button = ttk.Button(frm, text="Speak", command=self.run_app).grid(column=1, row=0)
        
        root.mainloop() #Start screen loop

    

