import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import tkinterdnd2 as tkdnd  # Drag & Drop support

# Function to handle folder selection via dialog
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        status_label.config(text=f"Selected: {folder_selected}", foreground="green")

# Function to handle drag & drop
def drop(event):
    folder = event.data.strip()
    if folder.startswith("{") and folder.endswith("}"):
        folder = folder[1:-1]  # Remove curly braces from Windows paths
    if os.path.isdir(folder):
        folder_path.set(folder)
        status_label.config(text=f"Selected: {folder}", foreground="green")
    else:
        messagebox.showerror("Error", "Invalid folder dropped!")

# Function to start the presentation
def start_presentation():
    if not folder_path.get():
        messagebox.showerror("Error", "Please select a folder first!")
        return

    # Run the presentation script
    messagebox.showinfo("Starting", "Starting the gesture-controlled presentation...")
    subprocess.Popen(["python", "gesture_presentation.py", folder_path.get()])

# Create main window
root = tkdnd.Tk()  # Enable Drag & Drop
root.title("Gesture-Controlled Presentation")
root.geometry("800x500")  # Set a fixed window size

# Set style
style = ttk.Style()
style.configure("TButton", font=("Arial", 14, "bold"), padding=10)
style.configure("TLabel", font=("Arial", 16, "bold"))

# Variable to store selected folder path
folder_path = tk.StringVar()

# UI Elements
title_label = ttk.Label(root, text="Gesture-Controlled Presentation System", font=("Arial", 20, "bold"))
title_label.pack(pady=15)

choose_button = ttk.Button(root, text="Choose Folder", command=select_folder)
choose_button.pack(pady=10)

# Drag & Drop Area
drop_label = ttk.Label(root, text="Drag & Drop a Folder Here", font=("Arial", 16), relief="solid", padding=20)
drop_label.pack(pady=10)
drop_label.drop_target_register(tkdnd.DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop)

status_label = ttk.Label(root, text="No folder selected", foreground="red", font=("Arial", 14))
status_label.pack(pady=10)

start_button = ttk.Button(root, text="Start Presentation", command=start_presentation)
start_button.pack(pady=15)

exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
