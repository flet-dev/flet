import base64
import hashlib
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def __generate_fernet_key(secret_key: str) -> bytes:
    key = hashlib.sha256(secret_key.encode()).digest()
    return base64.urlsafe_b64encode(key)


def __generate_fernet_key_kdf(secret_key: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    return base64.urlsafe_b64encode(kdf.derive(secret_key.encode("utf-8")))


def encrypt(plain_text: str, secret_key: str) -> str:
    salt = os.urandom(16)
    key = __generate_fernet_key_kdf(secret_key, salt)
    f = Fernet(key)
    return base64.urlsafe_b64encode(
        salt + f.encrypt(plain_text.encode("utf-8"))
    ).decode()


def decrypt(encrypted_data: str, secret_key: str) -> str:
    encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data)
    salt = encrypted_data_bytes[:16]
    key = __generate_fernet_key_kdf(secret_key, salt)
    f = Fernet(key)
    return f.decrypt(encrypted_data_bytes[16:]).decode("utf-8")
