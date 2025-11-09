# Day 4 File Upload - Client Side (Enhanced)
import socket
import os
from tqdm import tqdm

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002
BUFFER_SIZE = 4096

FILE_DIR = "test_files"  # Local folder containing files to send

# Ensure test_files folder exists
if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)
    print(f"[!] Folder '{FILE_DIR}' created. Add some files to upload.")
    exit()

# List available files
files = os.listdir(FILE_DIR)
if not files:
    print(f"[!] No files found in '{FILE_DIR}' folder. Please add some files first.")
    exit()

print(f"\nAvailable files in '{FILE_DIR}':")
print("=" * 40)
for i, file in enumerate(files, start=1):
    file_path = os.path.join(FILE_DIR, file)
    size = os.path.getsize(file_path)
    print(f"{i}. {file} ({size} bytes)")
print("=" * 40)

# Ask user to select file
choice = input("\nEnter the filename to send: ").strip()
filepath = os.path.join(FILE_DIR, choice)

if not os.path.exists(filepath):
    print(f"[!] File '{choice}' not found in '{FILE_DIR}'.")
    exit()

filesize = os.path.getsize(filepath)
print(f"[i] Preparing to send '{choice}' ({filesize} bytes)...")

# Create socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_HOST, SERVER_PORT))
print(f"[+] Connected to {SERVER_HOST}:{SERVER_PORT}")

# Send filename and filesize
s.send(f"{choice}|{filesize}".encode())

# Progress bar
progress = tqdm(range(filesize), f"Uploading {choice}", unit="B", unit_scale=True, unit_divisor=1024)

with open(filepath, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))

progress.close()

# Confirmation
response = s.recv(BUFFER_SIZE).decode()
if response == "UPLOAD_COMPLETE":
    print(f"[✓] File '{choice}' uploaded successfully.")
else:
    print("[!] Upload failed or server did not confirm.")

s.close()
