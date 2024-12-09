# Import necessary libraries
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ping3 import ping
import threading
import csv
from tkinter import filedialog

# Global variables
pinging = False  # Flag to indicate if pinging is currently active
csv_file_path = None  # Path of the selected CSV file
hosts_list = []  # List of hosts loaded from the CSV file
results_data = []  # List to store ping results (for saving to CSV)

def add_label_to_results(text):
    """
    Adds a label (message) to the scrollable results area in the GUI.
    Automatically scrolls to the bottom of the results.
    Also adds the data to the results_data list for CSV export.
    """
    global results_data
    # Extract information from the text (e.g., host, time, and status)
    if "responded in" in text:
        parts = text.split(" ")
        host = parts[0]
        time = parts[-2]  # Time in ms
        status = "Reachable"
        results_data.append({"Host": host, "Result Time (ms)": time, "Status": status})
    elif "is unreachable" in text:
        host = text.split(" ")[0]
        results_data.append({"Host": host, "Result Time (ms)": "N/A", "Status": "Unreachable"})

    # Display the result in the GUI
    result_label = ttk.Label(results_inner, text=text, anchor="w", wraplength=500)
    result_label.pack(padx=15, pady=5, fill="x")
    # Scroll to the bottom of the results
    results_canvas.update_idletasks()
    results_canvas.yview_moveto(1)

def browse_csv():
    """
    Opens a file dialog to select a CSV file. Reads the file and extracts valid hostnames
    or IP addresses. Updates the GUI to indicate how many hosts were loaded.
    """
    global csv_file_path, hosts_list
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:  # If a file was selected
        csv_file_path = file_path
        hosts_list = []  # Clear the previous list of hosts
        try:
            # Open and read the CSV file
            with open(csv_file_path, 'r') as f:
                reader = csv.reader(f)
                # Flatten the rows into a single list of hosts, removing empty values
                hosts_list = [item.strip() for row in reader for item in row if item.strip()]
                if not hosts_list:  # Check if the file is empty
                    add_label_to_results("CSV file is empty or contains no valid hosts.")
                    return
        except Exception as e:
            add_label_to_results(f"Error reading CSV: {e}")
            return

        # Update the entry field in the GUI to indicate success
        entry.delete(0, tk.END)
        entry.insert(0, f"Loaded {len(hosts_list)} host(s) from CSV")

def start_pinging():
    """
    Starts the pinging process. Depending on the user input:
    - If a CSV file was loaded, pings all hosts from the file.
    - If a hostname/IP is manually entered, pings that single host.
    """
    global pinging, csv_file_path, hosts_list
    pinging = True  # Set the flag to indicate pinging is active

    host = entry.get().strip()  # Get the text from the input field

    # If the input indicates a CSV file was loaded
    if host.startswith("Loaded") and hosts_list:
        # Start pinging all hosts from the CSV in a separate thread
        threading.Thread(target=ping_hosts_from_list, args=(hosts_list,), daemon=True).start()
        return

    # If no valid input was provided
    if host == "" or host.startswith("CSV:"):
        add_label_to_results("Enter a site URL or load a CSV file containing valid hosts.")
        return

    # Start pinging the manually entered host
    threading.Thread(target=ping_host, args=(host,), daemon=True).start()

def stop_pinging():
    """
    Stops the pinging process by setting the global 'pinging' flag to False.
    """
    global pinging
    pinging = False

def ping_host(host):
    """
    Pings a single host continuously until the user stops the process.
    - Displays whether the host is reachable or unreachable.
    """
    global pinging
    while pinging:  # Keep pinging while the flag is True
        try:
            response = ping(host, timeout=2)  # Ping the host with a 2-second timeout
            if response is None:  # If no response
                add_label_to_results(f"{host} is unreachable!")
            else:
                add_label_to_results(f"{host} responded in {response * 1000:.2f} ms")  # Convert to ms
        except Exception as e:
            add_label_to_results(f"Error pinging {host}: {e}")
            break

def ping_hosts_from_list(hosts):
    """
    Pings each host in the provided list sequentially. Stops if the user
    interrupts the process.
    """
    global pinging
    for host in hosts:
        if not pinging:  # Stop if the flag is False
            break
        try:
            response = ping(host, timeout=2)  # Ping the host
            if response is None:  # If no response
                add_label_to_results(f"{host} is unreachable!")
            else:
                add_label_to_results(f"{host} responded in {response * 1000:.2f} ms")
        except Exception as e:
            add_label_to_results(f"Error pinging {host}: {e}")

def save_results_to_csv():
    """
    Saves the collected ping results to a CSV file. The user chooses the save location.
    """
    global results_data
    if not results_data:
        add_label_to_results("No results to save.")
        return

    # Open a save dialog to choose the file location
    save_path = filedialog.asksaveasfilename(
        title="Save Results to CSV",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if save_path:  # If the user provides a file name
        try:
            # Write results to the CSV file
            with open(save_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["Host", "Result Time (ms)", "Status"])
                writer.writeheader()  # Write the header row
                writer.writerows(results_data)  # Write the results
            add_label_to_results(f"Results saved to {save_path}")
        except Exception as e:
            add_label_to_results(f"Error saving results: {e}")

# GUI Setup
root = ttk.Window(themename="darkly")  # Create a themed window
root.geometry("600x600")  # Set the window size
root.title("Network Monitor GUI")  # Set the window title

# Title label
label = ttk.Label(root, text="Network Monitoring Script", font=("Arial", 24))
label.pack(side=TOP, pady=10)

# Entry field for manual host input
entry = ttk.Entry(root, font=("Arial", 14))
entry.pack(side=TOP, padx=15, pady=5)

# Buttons for starting/stopping ping and browsing CSV
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

# Save results button
button_save = ttk.Button(root, text="Save Results to CSV", command=save_results_to_csv, bootstyle="success")
button_save.pack(side=BOTTOM, pady=10)

# Start the main event loop
root.mainloop()