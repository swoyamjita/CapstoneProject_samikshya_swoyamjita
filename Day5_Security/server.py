# Day 5 Secure File Upload Server with Authentication & Encryption
import socket
import os
import hashlib
from cryptography.fernet import Fernet
from utils.encryption import load_or_create_key


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5003
BUFFER_SIZE = 4096
UPLOAD_DIR = "uploads"
USERS_FILE = "users.txt"

# Load encryption key
fernet = Fernet(load_or_create_key())

# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load users
def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    username, password_hash = line.strip().split(":")
                    users[username] = password_hash
    return users

users = load_users()
print("[DEBUG] Loaded users:")
for u, p in users.items():
    print(f"   -> {u}: {p}")

# Start server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Secure Server listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, address = server_socket.accept()
    print(f"[+] Connection from {address}")

    try:
        # Step 1: Authentication
        auth_data = client_socket.recv(BUFFER_SIZE).decode()
        username, password = auth_data.split("|")

        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        print(f"[DEBUG] Computed hash: {hashed_pw}")

        if username in users and users[username] == hashed_pw:
            client_socket.send("AUTH_SUCCESS".encode())
            print(f"[✓] {username} authenticated successfully.")
        else:
            client_socket.send("AUTH_FAILED".encode())
            print(f"[!] Authentication failed for {username}")
            client_socket.close()
            continue

        # Step 2: Receive file metadata
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split("|")
        filesize = int(filesize)
        filepath = os.path.join(UPLOAD_DIR, filename)

        print(f"[→] Receiving encrypted file '{filename}' ({filesize} bytes) from {username}")

        # Step 3: Receive and decrypt data
        with open(filepath, "wb") as f:
            total_received = 0
            while total_received < filesize:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                decrypted = fernet.decrypt(data)
                f.write(decrypted)
                total_received += len(data)

        print(f"[✓] Secure file '{filename}' received and decrypted successfully from {username}")
        client_socket.send("UPLOAD_COMPLETE".encode())

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        client_socket.close()
