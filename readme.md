# Sniffer Application

## Introduction

The Sniffer application is a graphical tool designed for port scanning using the `tkinter` and `customtkinter` libraries for the GUI. It leverages threading for concurrent operations and includes features such as dark/light theme switching and a loading animation. The backend port scanning functionality is implemented using sockets in Python.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Dependencies](#dependencies)
5. [Configuration](#configuration)
6. [Documentation](#documentation)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)
9. [Contributors](#contributors)
10. [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/LeoGotardo/sniffer.git
    cd sniffer
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    python view.py
    ```

## Usage

1. **Starting the Application:**
    - Run `python view.py` to start the GUI Sniffer application.
    - To run `Sniffer` in terminal, check [Examples](#examples) > Command Line Usage

2. **Performing a Port Scan:**
    - Enter the target host, initial port, and final port in the respective fields.
    - Choose between scanning all ports or only the main ports using the toggle switch.
    - Click the "Scan" button to initiate the scan.

3. **Theme Switching:**
    - Toggle between dark and light themes using the theme button located at the bottom of the window.

## Features

- **Graphical User Interface:** Built with `customtkinter`, providing a modern and customizable interface.
- **Concurrent Scanning:** Utilizes threading to perform port scans without freezing the GUI.
- **Port Range Selection:** Option to scan a specific range of ports or only the main ports.
- **Theme Switching:** Allows users to switch between dark and light themes.
- **Loading Animation:** Displays a loading animation during port scans.

## Dependencies

- `customtkinter`
- `tkinter`
- `PIL` (Python Imaging Library)
- `ctypes`
- `sys`
- `sockets`

## Configuration

The configuration options are mostly handled through the GUI, including the host and port range input. The theme can be toggled between dark and light modes using the provided button.

## Documentation

### `view.py`

- **CustomThread**: A custom thread class extending `threading.Thread` with additional functionality to raise exceptions in the thread.
- **View**: The main GUI class handling all user interactions and displaying results.
    - `theme(button)`: Toggles between dark and light themes.
    - `askClose()`: Prompts the user to confirm before closing the application.
    - `scan()`: Initiates the port scan in a separate thread.
    - `isalive()`: Checks if the scanning thread is still running.
    - `loading()`: Sets up the loading page.
    - `scanScreen()`: Sets up the main screen for user input.
    - `showPorts()`: Displays the list of open ports.

### `portScanner.py`

- **PortScan**: The main class for performing port scans.
    - `scanPorts(ip, port_range, *rangePorts)`: Scans the specified ports and returns a list of open ports.

## Examples

### Command Line Usage

```sh
python3 portScanner.py 192.168.1.1 -a (for all ports, from 1 to 65535)
python3 portScanner.py 192.168.1.1 -a 1 65535
python3 portScanner.py 192.168.1.1 -m (for the main ports)
```

### GUI Usage

1. Open the Sniffer application.
2. Enter the host, initial port, and final port.
3. Click "Scan" to start scanning.

## Troubleshooting

- **Ports not scanning:** Ensure that the host and port inputs are correct and within valid ranges (1-65535).
- **Application not starting:** Check that all dependencies are installed and correctly imported.

## Contributors

- [Leonardo Gotardo](https://github.com/LeoGotardo) - Initial development
- [Espantalho](https://github.com/lilchoppa) - Backend development

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LeoGotardo/Sniffer/blob/main/LICENSE) file for details.
