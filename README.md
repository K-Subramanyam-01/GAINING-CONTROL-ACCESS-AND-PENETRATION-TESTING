# GAINING-CONTROL-ACCESSAND-PENETRATION-TESTING

## Overview

This repository contains various cybersecurity projects focused on network security, penetration testing, and ethical hacking. One of the key projects in this repository is a client-server application designed to execute remote commands and capture keystrokes using a keylogger.

## Project: Remote Command Execution and Keylogging

### Description

This project demonstrates a simple client-server architecture where the client can receive and execute commands from the server. Additionally, the client is capable of running a keylogger that captures keystrokes and sends the log file back to the server. This project is intended for educational purposes to understand the concepts of remote command execution and keylogging in the context of cybersecurity.

### Features

- **Client-Server Communication**: Establishes a connection between a client and a server using TCP sockets.
- **Remote Command Execution**: Allows the server to send various commands to the client for execution, including shutdown, restart, DOS attack, and more.
- **Keylogging**: Captures keystrokes on the client machine and sends the log file to the server.
- **File Transfer**: Supports sending and receiving files between the client and server.
- **Error Handling**: Includes basic error handling for connection issues and invalid commands.

### Components

- **Client Script** (`Ash-2.py`): A Python script that connects to the server, receives commands, executes them, and sends keylogger logs back to the server.
- **Server Script** (`masster-1.py`): A Python script that listens for incoming client connections, sends commands, and receives keylogger logs from the client.

### Switch Case Options

The server can send the following commands to the client:

- **1. Shutdown**: The client will execute a shutdown command.
- **2. Restart**: The client will execute a restart command.
- **3. DOS Attack**: The client will open a web browser and navigate to a specified URL to simulate a DOS attack.
- **4. Shantabhai**: The client will open a web browser and navigate to a specific YouTube video.
- **5. Send File**: The server will send a file to the client.
- **6. Remove File**: The client will remove a specified file.
- **7. Keylogger**: The client will start a keylogger, capture keystrokes, and send the log file to the server.
- **8. Exit**: The server will disconnect from the client.

### How to Run

1. **Setup the Server**:
   - Run the `masster-1.py` script on the server machine.
   - The server will listen for incoming connections and provide a menu to send commands to the client.

   ```bash
   python masster-1.py
   ```

2. **Setup the Client**:
   - Run the `Ash-2.py` script on the client machine.
   - The client will connect to the server and wait for commands.

   ```bash
   python Ash-2.py
   ```

3. **Executing Commands**:
   - Use the server menu to send commands to the client. The client will execute the commands and send the keylogger log file back to the server if the keylogger command is executed.

### Important Notes

- This project is for educational purposes only. Unauthorized use of keyloggers or remote command execution can be illegal and unethical.
- Ensure you have permission to run these scripts on the target machines.
- Modify the scripts to include proper security measures before using them in a real-world scenario.

### Future Enhancements

- Implement encryption for communication between the client and server.
- Add authentication mechanisms to ensure only authorized clients can connect to the server.
- Improve error handling and logging for better debugging and monitoring.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author

[K-Subramanyam-01](https://github.com/K-Subramanyam-01)
