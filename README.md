
# Network Monitoring GUI

A Python-based GUI application for monitoring network connectivity by pinging hosts (IP addresses or domain names). The application allows users to:
- Ping individual hosts or multiple hosts from a CSV file.
- View real-time results in a scrollable window.
- Save the results to a CSV file for later analysis.

This project uses the `ping3` library for network pings and `ttkbootstrap` for creating a modern, styled graphical interface.

---

## Features
- **Ping Single Hosts**: Enter a domain name or IP address to ping continuously.
- **Ping Multiple Hosts**: Select a CSV file containing hostnames or IPs, and the app will sequentially ping them.
- **Real-Time Results**: Displays the ping response time or connectivity status in a scrollable interface.
- **Save Results**: Export results to a CSV file with the following headers:
  - `Host`: The hostname or IP address.
  - `Result Time (ms)`: Response time in milliseconds (or `N/A` if unreachable).
  - `Status`: Either `Reachable` or `Unreachable`.

---

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `ping3`: For performing network pings.
  - `ttkbootstrap`: For building the GUI.
  - `tkinter`: Built-in Python library for GUI applications.

Install the required libraries using `pip`:
```bash
pip install ping3 ttkbootstrap
```

---

## How to Run

1. Clone or download the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Run the Python script:
   ```bash
   python network_monitor.py
   ```

3. Use the GUI to:
   - Enter a hostname or IP address in the input field to start pinging.
   - Browse and load a CSV file containing multiple hosts.
   - Start/Stop the pinging process using the respective buttons.
   - Save results to a CSV file using the "Save Results to CSV" button.

---

## CSV File Format

The application supports CSV files with the following format:
- Each row can contain one or more hostnames or IPs (comma-separated).
- Example:
  ```
  google.com
  8.8.8.8, example.com
  ```

---

## GUI Components

1. **Entry Field**: Input a single hostname or IP to ping.
2. **Buttons**:
   - **Start Ping**: Begins the pinging process.
   - **Stop Ping**: Stops the current pinging process.
   - **Browse CSV**: Allows users to load a CSV file with multiple hosts.
   - **Save Results to CSV**: Saves the displayed results to a file.
3. **Results Area**: Displays real-time ping results.

---

## Output CSV File

The saved CSV file will include the following headers:
- **Host**: The hostname or IP address pinged.
- **Result Time (ms)**: Response time in milliseconds (or `N/A` if the host is unreachable).
- **Status**: Indicates whether the host is `Reachable` or `Unreachable`.

Example output:
```csv
Host,Result Time (ms),Status
google.com,15.25,Reachable
8.8.8.8,25.50,Reachable
example.com,N/A,Unreachable
```

---

## Example Usage

1. **Ping a Single Host**:
   - Enter `google.com` in the input field and click `Start Ping`.
   - View the results in the scrollable area.

2. **Ping Hosts from a CSV File**:
   - Click `Browse CSV` and select a file containing hosts.
   - Click `Start Ping` to begin sequentially pinging the hosts.

3. **Save Results**:
   - Once the results are displayed, click `Save Results to CSV` to export them.

---

## Troubleshooting

1. **No Results Displayed**:
   - Ensure you entered a valid hostname or IP address.
   - If using a CSV file, check its format and contents.

2. **Dependencies Not Installed**:
   - Run `pip install ping3 ttkbootstrap` to install missing libraries.

3. **Permission Issues**:
   - Ensure you have write permissions for saving the results CSV file.

---

## Future Enhancements

- Add support for advanced ping options (e.g., count, timeout, TTL).
- Enable real-time charting of ping response times.
- Improve error handling for invalid hosts or unreachable networks.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it.
