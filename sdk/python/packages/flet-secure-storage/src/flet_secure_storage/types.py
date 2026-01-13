from dataclasses import dataclass
from enum import Enum

import flet as ft


@dataclass
class SecureStorageEvent(ft.Event["SecureStorage"]):  # type: ignore
    available: bool | None


class KeychainAccessibility(Enum):
    PASSCODE = "passcode"
    UNLOCKED = "unlocked"
    UNLOCKED_THIS_DEVICE = "unlocked_this_device"
    FIRST_UNLOCK = "first_unlock"
    FIRST_UNLOCK_THIS_DEVICE = "first_unlock_this_device"


class AccessControlFlag(Enum):
    DEVICE_PASSCODE = "device_passcode"
    BIOMETRY_ANY = "biometry_any"
    BIOMETRY_CURRENT_SET = "biometry_current_set"
    USER_PRESENCE = "user_presence"
    WATCH = "watch"
    OR = "or"
    AND = "and"
    APPLICATION_PASSWORD = "application_password"
    PRIVATE_KEY_USAGE = "private_key_usage"


class KeyCipherAlgorithm(Enum):
    RSA_ECB_PKCS1 = "RSA_ECB_PKCS1Padding"
    RSA_ECB_OAEP = "RSA_ECB_OAEPwithSHA_256andMGF1Padding"
    AES_GCM = "AES_GCM_NoPadding"


class StorageCipherAlgorithm(Enum):
    AES_CBC_PKCS7 = "AES_CBC_PKCS7Padding"
    AES_GCM = "AES_GCM_NoPadding"
