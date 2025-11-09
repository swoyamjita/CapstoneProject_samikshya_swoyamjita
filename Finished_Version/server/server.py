import socket
import os
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
from colorama import Fore, init
from utils.config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, UPLOAD_DIR, USERS_FILE, LOG_FILE, KEY_FILE
from utils.encryption import load_or_create_key

# Initialize color output
init(autoreset=True)

# Load encryption key
fernet = Fernet(load_or_create_key())

# =====================================================
# Utility Functions
# =====================================================

def log_event(message):
    """Log events with timestamps."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def load_users():
    """Load username-password-hash data from users.txt."""
    users = {}
    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 3:
                    username, plain, hashed = parts
                    users[username] = hashed
        print(Fore.CYAN + f"[DEBUG] Loaded users: {list(users.keys())}")
    except FileNotFoundError:
        print(Fore.RED + "[X] users.txt not found. Run add_user.py first.")
    return users

def authenticate_client(conn, users):
    """Authenticate incoming client."""
    try:
        data = conn.recv(BUFFER_SIZE).decode()
        username, password = data.split("|")
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        if username in users and users[username] == hashed_pw:
            conn.send("AUTH_SUCCESS".encode())
            print(Fore.GREEN + f"[✔] {username} authenticated successfully.")
            log_event(f"{username} logged in.")
            return username
        else:
            conn.send("AUTH_FAILED".encode())
            print(Fore.RED + f"[X] Authentication failed for {username}.")
            log_event(f"Failed login attempt for {username}.")
            return None
    except Exception as e:
        print(Fore.RED + f"[!] Auth error: {e}")
        return None

def receive_file(conn, username):
    """Receive encrypted file and save it."""
    filename = conn.recv(BUFFER_SIZE).decode()
    enc_data = b""

    while True:
        chunk = conn.recv(BUFFER_SIZE)
        if not chunk:
            break
        enc_data += chunk

    try:
        decrypted = fernet.decrypt(enc_data)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(decrypted)

        print(Fore.GREEN + f"[✔] Secure file '{filename}' received from {username}")
        log_event(f"{username} uploaded {filename}")
        conn.send("UPLOAD_COMPLETE".encode())
    except Exception as e:
        print(Fore.RED + f"[X] File decryption failed: {e}")
        conn.send("UPLOAD_FAILED".encode())

def start_server():
    """Start secure file upload server."""
    users = load_users()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(Fore.CYAN + f"[*] Secure Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(Fore.CYAN + f"[+] Connection from {addr}")

        username = authenticate_client(conn, users)
        if username:
            receive_file(conn, username)

        conn.close()
        print(Fore.YELLOW + f"[↳] Connection closed with {addr}")

if __name__ == "__main__":
    start_server()
