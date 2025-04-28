import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path # or use this for checking files in the folder

def add(a, b):
    return a + b

def files_exist(files):
    for file in files:
        if not os.path.exists(file):
            return False

    return False

def show_error_popup(message):
    # Create a root window, which will be hidden (because we only need the pop-up)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("File Missing", message)
    root.destroy()  # Close the root window after the pop-up is shown
    

if __name__ == "__main__":
    required_files = []
    if files_exist(required_files):
        pass 
    else:
        show_error_popup("One or more required files are missing.")