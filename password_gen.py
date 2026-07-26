import string
import secrets

def generate_password(length: int = 16, include_numbers: bool = True, include_symbols: bool = True) -> str:
    """Generates a cryptographically strong random password."""
    letters = string.ascii_letters
    digits = string.digits if include_numbers else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
    
    char_pool = letters + digits + symbols
    if not char_pool:
        char_pool = letters
        
    return ''.join(secrets.choice(char_pool) for _ in range(length))