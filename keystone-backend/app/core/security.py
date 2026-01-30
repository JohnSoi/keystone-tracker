"""Модуль для работы с хешами паролей."""

import bcrypt

from .consts import STR_ENCODED


def hash_password(password: str) -> str:
    """
    Хеширование пароля.

    Args:
        password (str): Пароль для хеширования.

    Returns:
        (str): Хешированный пароль.

    Examples:
        >>> from app.core import hash_password
        >>> hash_password("password") # Хеш пароля
    """
    pwd_bytes: bytes = password.encode(STR_ENCODED)
    salt: bytes = bcrypt.gensalt()
    hashed: bytes = bcrypt.hashpw(pwd_bytes, salt)

    return hashed.decode(STR_ENCODED)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Верификация пароля с помощью хеша.

    Args:
        plain_password (str): Пароль для верификации.
        hashed_password (str): Хешированный пароль.

    Returns:
        (bool): True, если пароль верифицирован, иначе False.

    Examples:
        >>> from app.core import verify_password, hash_password
        >>> verify_password("password", hash_password("password")) # True
        >>> verify_password("password", hash_password("password1")) # False
    """
    plain_pwd_bytes: bytes = plain_password.encode(STR_ENCODED)
    hashed_pwd_bytes: bytes = hashed_password.encode(STR_ENCODED)

    return bcrypt.checkpw(plain_pwd_bytes, hashed_pwd_bytes)
