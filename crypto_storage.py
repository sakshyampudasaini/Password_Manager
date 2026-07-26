import json
import os
from cryptography.fernet import Fernet
from typing import Dict, List

KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"

def load_or_create_key() -> bytes:
    """Loads existing key or generates a new master encryption key."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    with open(KEY_FILE, "rb") as f:
        return f.read()

KEY = load_or_create_key()
CIPHER = Fernet(KEY)

def save_accounts(accounts: List[Dict[str, str]]) -> None:
    """Encrypts and saves the list of account dictionaries."""
    raw_data = json.dumps(accounts).encode('utf-8')
    encrypted_data = CIPHER.encrypt(raw_data)
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted_data)

def load_accounts() -> List[Dict[str, str]]:
    """Loads and decrypts saved account credentials."""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, "rb") as f:
            encrypted_data = f.read()
            if not encrypted_data:
                return []
            decrypted_data = CIPHER.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode('utf-8'))
    except Exception:
        # Returns empty list if key is wrong or file is corrupted
        return []