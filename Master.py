import time
import socket
import os

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
host = "192.168.1.20"  # Replace this with the IP address of the server (local machine)
port = 8080

try:
    # Bind the socket to the host and port
    s.bind((host, port))
    print("\nWaiting for incoming connection...")
    s.listen(10)
    conn, addr = s.accept()

    print("\nClient is connected to the server now...\n")

    # Command loop
    while True:
        choice = input("1. Shutdown\n2. Restart\n3. DOS Attack\n4. Exit\nEnter your choice: ")
        
        if choice == "1":
            command = "shutdown"
            conn.sendall(command.encode())
            print("Shutdown command sent successfully. Waiting for confirmation...\n")
            data = conn.recv(1024).decode()
            if data:
                print("Shutdown command has been received and executed.\n")

        elif choice == "2":
            command = "restart"
            conn.sendall(command.encode())
            print("Restart command sent successfully. Waiting for confirmation...\n")
            data = conn.recv(1024).decode()
            if data:
                print("Restart command has been received and executed.\n")

        elif choice == "3":
            command = "DOS Attack"
            conn.sendall(command.encode())
            print("DOS Attack command sent successfully. Waiting for confirmation...\n")
            data = conn.recv(1024).decode()
            if data:
                print("DOS Attack command has been received and executed.\n")
                
        elif choice == "4":
            command = "exit"
            conn.sendall(command.encode())
            print("Exit command sent. Closing connection.")
            break

        else:
            print("Enter a valid choice.\n")

except socket.error as e:
    print(f"Socket error: {e}")
finally:
    conn.close()
    s.close()
