import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ping3 import verbose_ping
import platform
import threading
import io
import sys
from tkinter import filedialog

# Global variables
pinging = False
csv_file_path = None

def add_label_to_results(text):
    """Helper function to add labels to the results frame."""
    result_label = ttk.Label(results_inner, text=text)
    result_label.pack(padx=15, pady=5, anchor="w", fill="x")
    # Automatically scroll down
    results_canvas.update_idletasks()
    results_canvas.yview_moveto(1)

def browse_csv():
    """Open a file dialog to choose a CSV file and store its path."""
    global csv_file_path
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        csv_file_path = file_path
        # Update the entry field to indicate a CSV file is chosen
        entry.delete(0, tk.END)
        entry.insert(0, f"CSV: {file_path}")

def start_pinging():
    """Starts the pinging process."""
    global pinging, csv_file_path
    pinging = True

    host = entry.get().strip()

    # If no host was entered, but a CSV is selected, read from CSV
    if host == "" and csv_file_path:
        try:
            with open(csv_file_path, 'r') as f:
                lines = f.readlines()
                # Take the first non-empty line as the host
                lines = [line.strip() for line in lines if line.strip()]
                if not lines:
                    add_label_to_results("CSV file is empty or contains no valid hosts.")
                    return
                host = lines[0]
        except Exception as e:
            add_label_to_results(f"Error reading CSV: {e}")
            return

    if host == "":
        add_label_to_results("Enter a site URL or select a CSV file containing a host.")
        return

    # Run the pinging process in a separate thread to avoid freezing the GUI
    threading.Thread(target=ping_system, args=(host,), daemon=True).start()

def stop_pinging():
    """Stops the pinging process."""
    global pinging
    pinging = False

def ping_system(host):
    """Continuously pings the host until stopped."""
    global pinging
    while pinging:
        # Capture the stdout output of verbose_ping
        output = io.StringIO()
        sys.stdout = output  # Redirect stdout
        try:
            verbose_ping(host, count=1)
        finally:
            sys.stdout = sys.__stdout__  # Restore stdout

        # Get the captured output
        response = output.getvalue().strip()
        if "timed out" in response or "unreachable" in response:
            add_label_to_results(f"{host} is down!")
        else:
            add_label_to_results(response)

root = ttk.Window(themename="darkly")
root.geometry("600x400")
root.title("Network Monitor GUI")

label = ttk.Label(root, text="Network Monitoring Script", font=("Arial", 24))
label.pack(side=TOP, pady=10)

entry = ttk.Entry(root, font=("Arial", 14))
entry.pack(side=TOP, padx=15, pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(side=TOP, pady=5)

button_start = ttk.Button(button_frame, text="Start Ping", command=start_pinging, bootstyle="primary")
button_start.pack(side=LEFT, padx=10)

button_stop = ttk.Button(button_frame, text="Stop Ping", command=stop_pinging, bootstyle="danger")
button_stop.pack(side=LEFT, padx=10)

button_browse = ttk.Button(button_frame, text="Browse CSV", command=browse_csv, bootstyle="info")
button_browse.pack(side=LEFT, padx=10)

# Scrollable results frame
results_frame = ttk.Frame(root, padding=5, bootstyle="info")
results_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Canvas for scrollable content
results_canvas = tk.Canvas(results_frame, height=200)
results_canvas.pack(side="left", fill="both", expand=True)

# Scrollbar for the canvas
scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_canvas.yview)
scrollbar.pack(side="right", fill="y")

# Frame inside the canvas to hold results
results_inner = ttk.Frame(results_canvas)
results_inner.bind(
    "<Configure>",
    lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
)
results_canvas.create_window((0, 0), window=results_inner, anchor="nw")
results_canvas.configure(yscrollcommand=scrollbar.set)

root.mainloop()
