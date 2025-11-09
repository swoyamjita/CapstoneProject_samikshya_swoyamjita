import socket
import os

HOST = '127.0.0.1'
PORT = 5050
BUFFER_SIZE = 4096
DOWNLOAD_FOLDER = 'downloads'

# Ensure downloads folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"[+] Connected to server {HOST}:{PORT}")

# Receive file list
files = client_socket.recv(BUFFER_SIZE).decode()
print("\nAvailable files on server (from 'test_files'):\n")
print(files)

selected_file = input("\nEnter the name of the file you want to download: ")
client_socket.send(selected_file.encode())

# Check if the file exists on the server
response = client_socket.recv(BUFFER_SIZE).decode()
if response == "FILE_NOT_FOUND":
    print(f"[!] The file '{selected_file}' does not exist on the server.")
else:
    filepath = os.path.join(DOWNLOAD_FOLDER, selected_file)
    with open(filepath, "wb") as f:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)

    print(f"[✓] File '{selected_file}' downloaded successfully to '{DOWNLOAD_FOLDER}/'")
    print(f"[💾] Full path: {os.path.abspath(filepath)}")

client_socket.close()
