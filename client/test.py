import socket
import os
import sys

# Create a socket object
client_socket = socket.socket()

# Get the server host name or IP address
server_host = input("Enter the server host name or IP address: ")

# Reserve a port for the service
port = 12345

# Connect to the server
client_socket.connect((server_host, port))

while True:
    # Prompt the user for a request
    request = input("Enter a request (transfer_file, delete_file, create_directory, browse_directory, or exit): ")

    # Send the request to the server
    client_socket.sendall(request.encode())

    if request.startswith("transfer_file"):
        # Receive a file from the server
        file_name = request.split(" ")[1]
        with open(file_name, "wb") as file:
            data = client_socket.recv(1024)
            while data:
                file.write(data)
                data = client_socket.recv(1024)
        print("File transferred successfully")
    elif request.startswith("delete_file"):
        # Delete a file on the client
        response = client_socket.recv(1024).decode()
        print(response)
    elif request.startswith("create_directory"):
        # Create a directory on the client
        response = client_socket.recv(1024).decode()
        print(response)
    elif request.startswith("browse_directory"):
        # Browse the contents of a directory on the client
        response = client_socket.recv(1024).decode()
        print(response)
    elif request == "exit":
        break
    else:
        # Print an error message if the request is not recognized
        response = client_socket.recv(1024).decode()
        print(response)

# Close the connection with the server
client_socket.close()