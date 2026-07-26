import string
import secrets
from typing import Tuple

def generate_password(length: int = 16, include_numbers: bool = True, include_symbols: bool = True) -> str:
    """Generates a cryptographically secure random password."""
    letters = string.ascii_letters
    digits = string.digits if include_numbers else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
    
    char_pool = letters + digits + symbols
    if not char_pool:
        char_pool = letters
        
    return ''.join(secrets.choice(char_pool) for _ in range(length))

def calculate_strength(password: str) -> Tuple[int, str, str]:
    """
    Evaluates password strength.
    Returns: (score_0_to_100, label_text, color_hex)
    """
    if not password:
        return 0, "None", "#808080"
        
    score = 0
    length = len(password)
    
    # Length points
    if length >= 8: score += 20
    if length >= 12: score += 20
    if length >= 16: score += 20
    
    # Diversity points
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    types_count = sum([has_upper, has_lower, has_digit, has_symbol])
    score += types_count * 10

    if score < 40:
        return score, "Weak 🔴", "#e74c3c"
    elif score < 70:
        return score, "Medium 🟡", "#f1c40f"
    else:
        return score, "Strong 🟢", "#2ecc71"
