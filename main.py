import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ping3 import verbose_ping
import platform
import threading
import io
import sys

# Global variable to control pinging process
pinging = False

def add_label_to_results(text):
    """Helper function to add labels to the results frame."""
    result_label = ttk.Label(results_inner, text=text)
    result_label.pack(padx=15, pady=5, anchor="w", fill="x")
    # Automatically scroll down
    results_canvas.update_idletasks()
    results_canvas.yview_moveto(1)

def start_pinging():
    """Starts the pinging process."""
    global pinging
    pinging = True
    host = entry.get()
    if host == "":
        add_label_to_results("Enter a site URL. E.g.: google.com")
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

button_start = ttk.Button(root, text="Start Ping", command=start_pinging, bootstyle="primary")
button_start.pack(side=LEFT, padx=10, pady=5)

button_stop = ttk.Button(root, text="Stop Ping", command=stop_pinging, bootstyle="danger")
button_stop.pack(side=LEFT, padx=10, pady=5)

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
