# Hash de contraseñas con bcrypt.

import bcrypt


def hash_password(plain_password: str) -> str:
    # Hashea una contraseña en texto plano.
    # Devuelve el hash como string (para guardar en la BD).
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verifica una contraseña contra el hash guardado.
    # Devuelve True si coinciden.
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False
