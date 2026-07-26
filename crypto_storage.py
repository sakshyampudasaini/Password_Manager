import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Dict, List, Optional

DATA_FILE = "vault.json"
SALT_FILE = "salt.bin"

def get_or_create_salt() -> bytes:
    """Retrieves existing salt or generates a new one for key derivation."""
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derives a strong AES-256 Fernet key from the user's master password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=400000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

class VaultStorage:
    def __init__(self):
        self.salt = get_or_create_salt()
        self.fernet: Optional[Fernet] = None

    def vault_exists(self) -> bool:
        """Checks if a vault file already exists."""
        return os.path.exists(DATA_FILE)

    def initialize_vault(self, master_password: str) -> None:
        """Sets up a brand new vault encrypted with the provided master password."""
        key = derive_key(master_password, self.salt)
        self.fernet = Fernet(key)
        self.save_accounts([])

    def verify_and_unlock(self, master_password: str) -> bool:
        """Attempts to unlock the vault. Returns True if password is correct."""
        try:
            key = derive_key(master_password, self.salt)
            candidate_fernet = Fernet(key)
            with open(DATA_FILE, "rb") as f:
                encrypted_data = f.read()
            # Try decrypting — raises an exception if the master password is wrong
            decrypted_data = candidate_fernet.decrypt(encrypted_data)
            json.loads(decrypted_data.decode('utf-8'))
            self.fernet = candidate_fernet
            return True
        except Exception:
            return False

    def save_accounts(self, accounts: List[Dict[str, str]]) -> None:
        """Encrypts and writes the accounts list to disk."""
        if not self.fernet:
            raise PermissionError("Vault is locked.")
        raw_data = json.dumps(accounts).encode('utf-8')
        encrypted_data = self.fernet.encrypt(raw_data)
        with open(DATA_FILE, "wb") as f:
            f.write(encrypted_data)

    def load_accounts(self) -> List[Dict[str, str]]:
        """Decrypts and loads the accounts list."""
        if not self.fernet or not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception:
            return []
