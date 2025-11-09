from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def load_or_create_key():
    """Load the encryption key or create a new one if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key
