import socket
import os
import sys

# Create a socket object
server_socket = socket.socket()

# Get local machine name
host = socket.gethostname()
print(host)
# Reserve a port for the service
port = 12345

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections from clients
server_socket.listen(5)

print("Server is listening for incoming connections...")

while True:
    # Establish a connection with a client
    client_socket, client_address = server_socket.accept()
    print("Got connection from", client_address)

    # Receive the request from the client
    request = client_socket.recv(1024).decode()

    # Parse the request to determine the action
    if request.startswith("transfer_file"):
        # Transfer a file from the server to the client
        file_name = request.split(" ")[1]
        if os.path.exists(file_name):
            with open(file_name, "rb") as file:
                data = file.read()
                client_socket.sendall(data)
        else:
            # Send an error message if the file does not exist
            client_socket.sendall("error: file not found".encode())
    elif request.startswith("delete_file"):
        # Delete a file on the server
        file_name = request.split(" ")[1]
        if os.path.exists(file_name):
            os.remove(file_name)
            client_socket.sendall("file deleted".encode())
        else:
            # Send an error message if the file does not exist
            client_socket.sendall("error: file not found".encode())
    elif request.startswith("create_directory"):
        # Create a directory on the server
        directory_name = request.split(" ")[1]
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            client_socket.sendall("directory created".encode())
        else:
            # Send an error message if the directory already exists
            client_socket.sendall("error: directory already exists".encode())
    elif request.startswith("browse_directory"):
        # Browse the contents of a directory on the server
        directory_name = request.split(" ")[1]
        if os.path.exists(directory_name):
            contents = os.listdir(directory_name)
            client_socket.sendall("\n".join(contents).encode())
        else:
            # Send an error message if the directory does not exist
            client_socket.sendall("error: directory not found".encode())
    else:
        # Send an error message if the request is not recognized
        client_socket.sendall("error: invalid request".encode())

    # Close the connection with the client
    client_socket.close()
