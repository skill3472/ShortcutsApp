import hashlib
import os
from datetime import UTC, datetime, timedelta

import jwt

from config import settings

_ALGORITHM = "HS256"
_TOKEN_TTL = timedelta(hours=8)


def hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return f"{salt.hex()}:{key.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    salt_hex, key_hex = password_hash.split(":")
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return key.hex() == key_hex


def create_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.now(UTC) + _TOKEN_TTL}
    return jwt.encode(payload, settings.secret_key, algorithm=_ALGORITHM)


def decode_token(token: str) -> int:
    payload = jwt.decode(token, settings.secret_key, algorithms=[_ALGORITHM])
    return int(payload["sub"])
