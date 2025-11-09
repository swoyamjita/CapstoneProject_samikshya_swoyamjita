import socket
import os
from tqdm import tqdm
from cryptography.fernet import Fernet
from colorama import Fore, init
from utils.config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, CLIENT_UPLOAD_DIR
from utils.encryption import load_or_create_key

# Initialize
init(autoreset=True)
fernet = Fernet(load_or_create_key())

def list_client_files():
    """List all files available in client/uploads/ directory."""
    print(Fore.CYAN + "\n=== Files Available in client/uploads/ ===")
    if not os.path.exists(CLIENT_UPLOAD_DIR):
        print(Fore.RED + "[X] Uploads folder not found.")
        return []

    files = os.listdir(CLIENT_UPLOAD_DIR)
    if not files:
        print(Fore.YELLOW + "[!] No files found in client/uploads/")
    else:
        for idx, file in enumerate(files, 1):
            print(Fore.WHITE + f"{idx}. {file}")
    print(Fore.CYAN + "========================================\n")
    return files

def connect_to_server():
    """Establish socket connection."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
    print(Fore.GREEN + f"[+] Connected to {SERVER_HOST}:{SERVER_PORT}")
    return s

def authenticate(s, username, password):
    """Authenticate with server."""
    s.send(f"{username}|{password}".encode())
    response = s.recv(BUFFER_SIZE).decode()
    if response == "AUTH_SUCCESS":
        print(Fore.GREEN + "[✔] Authentication successful.")
        return True
    else:
        print(Fore.RED + "[X] Authentication failed.")
        return False

def send_file(s, filename):
    """Encrypt and send file to server."""
    filepath = os.path.join(CLIENT_UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        print(Fore.RED + f"[X] File '{filename}' not found.")
        return

    with open(filepath, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)
    s.send(filename.encode())

    progress = tqdm(total=len(encrypted), unit="B", unit_scale=True, desc=f"Sending {filename}")
    s.sendall(encrypted)
    progress.close()

    print(Fore.GREEN + f"[✔] File '{filename}' sent securely.")

def start_client():
    """Main client execution."""
    print(Fore.YELLOW + "=== Secure File Upload Client ===")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    s = connect_to_server()

    if authenticate(s, username, password):
        # 🔹 Show file list before asking user input
        files = list_client_files()
        filename = input(Fore.WHITE + "Enter filename to send (from 'client/uploads/'): ").strip()
        if filename not in files:
            print(Fore.RED + f"[X] File '{filename}' not found in client/uploads/")
            s.close()
            return

        send_file(s, filename)
        response = s.recv(BUFFER_SIZE).decode()
        if response == "UPLOAD_COMPLETE":
            print(Fore.GREEN + "[✔] Server confirmed upload completion.")
    else:
        print(Fore.RED + "[X] Authentication failed. Connection closed.")

    s.close()
    print(Fore.YELLOW + "[↳] Connection closed.")

if __name__ == "__main__":
    start_client()
