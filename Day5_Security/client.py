# Day 5 Secure File Upload Client with File Listing & Encryption
import socket
import os
import hashlib
from tqdm import tqdm
from cryptography.fernet import Fernet
from utils.encryption import load_or_create_key

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5003
BUFFER_SIZE = 4096
TEST_FOLDER = "test_files"

# Ensure folder exists
os.makedirs(TEST_FOLDER, exist_ok=True)

# Load encryption key
fernet = Fernet(load_or_create_key())

# Step 1: Authentication
username = input("Enter username: ").strip()
password = input("Enter password: ").strip()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_HOST, SERVER_PORT))
print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")

s.send(f"{username}|{password}".encode())

response = s.recv(BUFFER_SIZE).decode()
if response != "AUTH_SUCCESS":
    print("[!] Authentication failed. Connection closed.")
    s.close()
    exit()
print("[✓] Authentication successful. Secure channel established.\n")

# Step 2: File Listing
files = os.listdir(TEST_FOLDER)
if not files:
    print(f"[!] No files found in '{TEST_FOLDER}' folder. Add files to continue.")
    s.close()
    exit()

print(f"Available files in '{TEST_FOLDER}':")
print("=" * 40)
for i, file in enumerate(files, start=1):
    file_path = os.path.join(TEST_FOLDER, file)
    size = os.path.getsize(file_path)
    print(f"{i}. {file} ({size} bytes)")
print("=" * 40)

# Step 3: Choose file
filename = input("\nEnter filename to send: ").strip()
filepath = os.path.join(TEST_FOLDER, filename)

if not os.path.exists(filepath):
    print(f"[!] File '{filename}' not found in '{TEST_FOLDER}'.")
    s.close()
    exit()

filesize = os.path.getsize(filepath)
print(f"[i] Preparing to send '{filename}' ({filesize} bytes) securely...")

# Step 4: Send metadata
s.send(f"{filename}|{filesize}".encode())

# Step 5: Encrypt & send file
progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

with open(filepath, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        encrypted = fernet.encrypt(bytes_read)
        s.sendall(encrypted)
        progress.update(len(bytes_read))

progress.close()
print(f"[✓] File '{filename}' sent securely.")

# Step 6: Confirmation
confirmation = s.recv(BUFFER_SIZE).decode()
if confirmation == "UPLOAD_COMPLETE":
    print(f"[✓] Server confirmed upload completion for '{filename}'.")
else:
    print("[!] Server did not confirm upload completion.")

s.close()
