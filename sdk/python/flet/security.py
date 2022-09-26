import base64
import hashlib

from cryptography.fernet import Fernet


def __generate_fernet_key(password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt(plain_text: str, password: str) -> str:
    key = __generate_fernet_key(password)
    f = Fernet(key)
    return base64.urlsafe_b64encode(f.encrypt(plain_text.encode("utf-8"))).decode()


def decrypt(encrypted_data: str, password: str) -> str:
    encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data)
    key = __generate_fernet_key(password)
    f = Fernet(key)
    return f.decrypt(encrypted_data_bytes).decode("utf-8")
