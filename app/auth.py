"""
Modulo de autenticacion.
"""

import os
import secrets
from dotenv import load_dotenv

def validate_credentials(username: str, password: str) -> bool:
    """
    Valida las credenciales proporcionadas contra las guardadas.

    Args:
        username (str): Nombre de usuario a validar.
        password (str): Contraseña a validar.

    Returns:
        bool: True si las credenciales son validas, False de otra manera.
    """
    load_dotenv()
    valid_users = os.getenv("USERS", "").split(",")
    valid_passwords = os.getenv("PASSWORDS", "").split(",")
    creds = dict(zip(valid_users, valid_passwords))
    expected_password = creds.get(username)
    return secrets.compare_digest(password, expected_password or "")
