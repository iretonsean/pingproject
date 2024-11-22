"""

Author: Sean Ireton
Program Name: SuperPinger
Version: 2.0.0
CIS 201 Project (Fall 2024)

Description: Pinging tool for devices connected to my LAN and WAN.
Objective: Ping devices and websites successfully, then log responses to an external file.
Libraries to use:
    Ping Libraries
        ping3 (https://pypi.org/project/ping3/)
        subprocess
    Data Handling
        Pandas


"""

# LIBRARY IMPORTS
###############################################################################################

import tkinter as tk
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ping3 import ping, verbose_ping

def ping_system():
    host = entry.get()
    response = os.system(f"ping -n 1 {host}")

    if host == "":
        label = ttk.Label(root, text="Enter a site URL. E.g.: google.com")
        label.pack()
    elif response == 0:
        label = ttk.Label(root, text=f"{host} is up!")
        label.pack()
    else:
        label = ttk.Label(root, text=f"{host} is down!")
        label.pack()

root = ttk.Window(themename="darkly")
root.title("Network Monitor GUI")

root.geometry("600x400")

label = ttk.Label(root, text="Network Monitoring Script", font=("Arial", 24))
label.pack(anchor="center", pady=20)

entry = ttk.Entry(root, font=("Arial", 14))
entry.pack()

button = ttk.Button(root, text="ping", command=ping_system)
button.pack(pady=10)

result_label = ttk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)


root.mainloop()

# print("network monitoring script")
# hosts = ["google.com", "yahoo.com", "bing.com"]
# for host in hosts:
#     ping_system(host)