import base64
import hashlib
import os

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError as e:
    raise ImportError(
        'Install "cryptography" Python package to use Flet security utils.'
    ) from e


def __generate_fernet_key(secret_key: str) -> bytes:
    """
    Derives a deterministic Fernet-compatible key from `secret_key`.

    The key is produced by hashing `secret_key` with SHA-256 and URL-safe
    Base64-encoding the 32-byte digest.

    Args:
        secret_key: Source secret used to derive the key.

    Returns:
        URL-safe Base64 key bytes suitable for `Fernet`.
    """
    key = hashlib.sha256(secret_key.encode()).digest()
    return base64.urlsafe_b64encode(key)


def __generate_fernet_key_kdf(secret_key: str, salt: bytes) -> bytes:
    """
    Derives a Fernet-compatible key using PBKDF2-HMAC-SHA256.

    This function uses 600,000 iterations and a caller-provided random `salt`, then
    URL-safe Base64-encodes the derived 32-byte key.

    Args:
        secret_key: Source secret used for key derivation.
        salt: Salt bytes used by PBKDF2.

    Returns:
        URL-safe Base64 key bytes suitable for `Fernet`.
    """
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000)
    return base64.urlsafe_b64encode(kdf.derive(secret_key.encode("utf-8")))


def encrypt(plain_text: str, secret_key: str) -> str:
    """
    Encrypts UTF-8 text using Fernet with a per-message salt-derived key.

    Output format is `base64url(salt + token)`, where:
    - `salt` is 16 random bytes;
    - `token` is a Fernet token encrypted with a key derived from `secret_key` and
      `salt`.

    Args:
        plain_text: Text to encrypt.
        secret_key: Secret used to derive the encryption key.

    Returns:
        URL-safe Base64 string containing salt-prefixed encrypted payload.
    """
    salt = os.urandom(16)
    key = __generate_fernet_key_kdf(secret_key, salt)
    f = Fernet(key)
    return base64.urlsafe_b64encode(
        salt + f.encrypt(plain_text.encode("utf-8"))
    ).decode()


def decrypt(encrypted_data: str, secret_key: str) -> str:
    """
    Decrypts data produced by [`encrypt()`][(m).encrypt].

    Input format must be `base64url(salt + token)`, where the first 16 bytes are
    the PBKDF2 salt and the remaining bytes are a Fernet token.

    Args:
        encrypted_data: URL-safe Base64 payload returned by [`encrypt()`][(m).encrypt].
        secret_key: Secret used to derive the decryption key.

    Returns:
        Decrypted UTF-8 text.

    Raises:
        binascii.Error: If `encrypted_data` is not valid Base64.
        cryptography.fernet.InvalidToken: If the token cannot be authenticated or
            decrypted with the derived key.
    """
    encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data)
    salt = encrypted_data_bytes[:16]
    key = __generate_fernet_key_kdf(secret_key, salt)
    f = Fernet(key)
    return f.decrypt(encrypted_data_bytes[16:]).decode("utf-8")


def encrypt_aes_gcm_256(plain_text: str, secret_key: str) -> str:
    """
    Encrypts UTF-8 text using AES-GCM with a 256-bit key.

    Output format is `base64url(salt + nonce + ciphertext_and_tag)`, where:
    - `salt` is 16 random bytes used for PBKDF2 key derivation;
    - `nonce` is 32 random bytes used by AES-GCM;
    - `ciphertext_and_tag` is the AES-GCM output.

    Key derivation:
    1. derive a salted key with
        [`__generate_fernet_key_kdf()`][(m).__generate_fernet_key_kdf];
    2. hash that value with SHA-256;
    3. use the first 32 bytes of the hex digest text as the AES key.

    Args:
        plain_text: Text to encrypt.
        secret_key: Secret used to derive the encryption key.

    Returns:
        URL-safe Base64 string containing salt, nonce, and encrypted payload.
    """
    nonce = os.urandom(32)
    salt = os.urandom(16)
    key = __generate_fernet_key_kdf(secret_key, salt)
    key = hashlib.sha256(key).hexdigest()
    ag = AESGCM(key[:32].encode())
    return base64.urlsafe_b64encode(
        salt + nonce + ag.encrypt(nonce, plain_text.encode("utf-8"), None)
    ).decode("utf-8")


def decrypt_aes_gcm_256(encrypted_data: str, secret_key: str) -> str:
    """
    Decrypts data produced by [`encrypt_aes_gcm_256()`][(m).encrypt_aes_gcm_256].

    Input format must be `base64url(salt + nonce + ciphertext_and_tag)`, where the
    first 16 bytes are salt and the next 32 bytes are AES-GCM nonce.

    Args:
        encrypted_data: URL-safe Base64 payload returned by
            [`encrypt_aes_gcm_256()`][(m).encrypt_aes_gcm_256].
        secret_key: Secret used to derive the decryption key.

    Returns:
        Decrypted UTF-8 text.

    Raises:
        binascii.Error: If `encrypted_data` is not valid Base64.
        cryptography.exceptions.InvalidTag: If authentication fails during AES-GCM
            decryption.
    """
    ciphertext_data_in_bytes = base64.urlsafe_b64decode(encrypted_data)
    salt = ciphertext_data_in_bytes[:16]
    key = __generate_fernet_key_kdf(secret_key, salt)
    key = hashlib.sha256(key).hexdigest()
    ag = AESGCM(key[:32].encode())
    return ag.decrypt(
        ciphertext_data_in_bytes[16:48], ciphertext_data_in_bytes[48:], None
    ).decode("utf-8")
