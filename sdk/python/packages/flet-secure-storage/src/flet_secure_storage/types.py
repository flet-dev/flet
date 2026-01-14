from dataclasses import dataclass
from enum import Enum
from typing import Optional

import flet as ft


class KeychainAccessibility(Enum):
    """
    KeyChain accessibility attributes as defined here:
    https://developer.apple.com/documentation/security/ksecattraccessible?language=objc
    """

    PASSCODE = "passcode"
    """
    The data in the keychain can only be accessed when the device is unlocked.

    Only available if a passcode is set on the device.
    Items with this attribute do not migrate to a new device.
    """

    UNLOCKED = "unlocked"
    """
    The data in the keychain item can be accessed only while
    the device is unlocked by the user.
    """

    UNLOCKED_THIS_DEVICE = "unlocked_this_device"
    """
    The data in the keychain item can be accessed only while
    the device is unlocked by the user.

    Items with this attribute do not migrate to a new device
    """

    FIRST_UNLOCK = "first_unlock"
    """
    The data in the keychain item cannot be accessed after a restart until
    the device has been unlocked once by the user.
    """

    FIRST_UNLOCK_THIS_DEVICE = "first_unlock_this_device"
    """
    The data in the keychain item cannot be accessed after
    a restart until the device has been unlocked once by the user.

    Items with this attribute do not migrate to a new device.
    """


class AccessControlFlag(Enum):
    """
    Keychain access control flags that define security conditions for accessing items.
    These flags can be combined to create complex access control policies.
    """

    DEVICE_PASSCODE = "device_passcode"
    """
    Constraint to access an item with a passcode.
    """

    BIOMETRY_ANY = "biometry_any"
    """
    Constraint to access an item with biometrics (Touch ID/Face ID).
    """

    BIOMETRY_CURRENT_SET = "biometry_current_set"
    """
    Constraint to access an item with the currently enrolled biometrics.
    """

    USER_PRESENCE = "user_presence"
    """
    Constraint to access an item with either biometry or passcode.
    """

    WATCH = "watch"
    """
    Constraint to access an item with a paired watch.
    """

    OR = "or"
    """
    Combine multiple constraints with an OR operation.
    """

    AND = "and"
    """
    Combine multiple constraints with an AND operation.
    """

    APPLICATION_PASSWORD = "application_password"
    """
    Use an application-provided password for encryption.
    """

    PRIVATE_KEY_USAGE = "private_key_usage"
    """
    Enable private key usage for signing operations.
    """


class KeyCipherAlgorithm(Enum):
    """
    Algorithm used to encrypt/wrap the secret key in Android KeyStore.
    """

    RSA_ECB_PKCS1 = "RSA_ECB_PKCS1Padding"
    """
    Legacy RSA/ECB/PKCS1Padding for backwards compatibility.
    """

    RSA_ECB_OAEP = "RSA_ECB_OAEPwithSHA_256andMGF1Padding"
    """
    RSA/ECB/OAEPWithSHA-256AndMGF1Padding (default, API 23+).
    """

    AES_GCM = "AES_GCM_NoPadding"
    """
    AES/GCM/NoPadding for KeyStore-based key wrapping (supports biometrics).
    """


class StorageCipherAlgorithm(Enum):
    """
    Algorithm used to encrypt stored data.
    """

    AES_CBC_PKCS7 = "AES_CBC_PKCS7Padding"
    """
    Legacy AES/CBC/PKCS7Padding for backwards compatibility.
    """

    AES_GCM = "AES_GCM_NoPadding"
    """
    AES/GCM/NoPadding (default, API 23+).
    """


@dataclass
class SecureStorageEvent(ft.Event["SecureStorage"]):  # type: ignore
    available: Optional[bool]
