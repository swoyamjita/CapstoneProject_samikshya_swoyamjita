import os
import hashlib

USERS_FILE = "server/users.txt"

def hash_password(password: str) -> str:
    """Return SHA256 hash of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username: str, password: str):
    """Add a new user with plaintext and hashed password."""
    os.makedirs("server", exist_ok=True)
    hashed = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{password}:{hashed}\n")
    print(f"[+] User '{username}' added successfully.")

if __name__ == "__main__":
    username = input("Enter new username: ").strip()
    password = input("Enter password: ").strip()
    add_user(username, password)
