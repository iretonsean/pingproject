import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ping3 import ping
import threading
import csv
from tkinter import filedialog

# Global variables
pinging = False
csv_file_path = None
hosts_list = []

def add_label_to_results(text):
    """Helper function to add labels to the results frame."""
    result_label = ttk.Label(results_inner, text=text, anchor="w", wraplength=500)
    result_label.pack(padx=15, pady=5, fill="x")
    # Automatically scroll down
    results_canvas.update_idletasks()
    results_canvas.yview_moveto(1)

def browse_csv():
    """Open a file dialog to choose a CSV file and extract hostnames."""
    global csv_file_path, hosts_list
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        csv_file_path = file_path
        hosts_list = []  # Clear previous host list
        try:
            with open(csv_file_path, 'r') as f:
                reader = csv.reader(f)
                # Flatten CSV content to a list of hosts
                hosts_list = [item.strip() for row in reader for item in row if item.strip()]
                if not hosts_list:
                    add_label_to_results("CSV file is empty or contains no valid hosts.")
                    return
        except Exception as e:
            add_label_to_results(f"Error reading CSV: {e}")
            return

        # Update the entry field to indicate a CSV file is chosen
        entry.delete(0, tk.END)
        entry.insert(0, f"Loaded {len(hosts_list)} host(s) from CSV")

def start_pinging():
    """Starts the pinging process."""
    global pinging, csv_file_path, hosts_list
    pinging = True

    host = entry.get().strip()

    # If no host was entered, but hosts are loaded from the CSV
    if host.startswith("Loaded") and hosts_list:
        threading.Thread(target=ping_hosts_from_list, args=(hosts_list,), daemon=True).start()
        return

    # If a single host is entered manually
    if host == "" or host.startswith("CSV:"):
        add_label_to_results("Enter a site URL or load a CSV file containing valid hosts.")
        return

    # Start pinging a single host
    threading.Thread(target=ping_host, args=(host,), daemon=True).start()

def stop_pinging():
    """Stops the pinging process."""
    global pinging
    pinging = False

def ping_host(host):
    """Pings a single host continuously until stopped."""
    global pinging
    while pinging:
        try:
            response = ping(host, timeout=2)
            if response is None:
                add_label_to_results(f"{host} is unreachable!")
            else:
                add_label_to_results(f"{host} responded in {response * 1000:.2f} ms")
        except Exception as e:
            add_label_to_results(f"Error pinging {host}: {e}")
            break

def ping_hosts_from_list(hosts):
    """Pings multiple hosts from a list."""
    global pinging
    for host in hosts:
        if not pinging:
            break
        try:
            response = ping(host, timeout=2)
            if response is None:
                add_label_to_results(f"{host} is unreachable!")
            else:
                add_label_to_results(f"{host} responded in {response * 1000:.2f} ms")
        except Exception as e:
            add_label_to_results(f"Error pinging {host}: {e}")

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
