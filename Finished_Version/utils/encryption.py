from cryptography.fernet import Fernet
import os
from utils.config import KEY_FILE

def load_or_create_key():
    """Load an existing Fernet key or create a new one."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key
