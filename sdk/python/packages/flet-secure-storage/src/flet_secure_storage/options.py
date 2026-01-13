from dataclasses import dataclass, field
from datetime import datetime

from flet_secure_storage.types import (
    AccessControlFlag,
    KeychainAccessibility,
    KeyCipherAlgorithm,
    StorageCipherAlgorithm,
)


@dataclass
class AndroidOptions:
    reset_on_error: bool = False
    migrate_on_algorithm_change: bool = False
    enforce_biometrics: bool = True
    key_cipher_algorithm: KeyCipherAlgorithm = KeyCipherAlgorithm.RSA_ECB_OAEP
    storage_cipher_algorithm: StorageCipherAlgorithm = StorageCipherAlgorithm.AES_GCM
    shared_preferences_name: str | None = None
    preferences_key_prefix: str | None = None
    biometric_prompt_title: str = "Authenticate to access"
    biometric_prompt_subtitle: str = "Use biometrics or device credentials"


@dataclass
class AppleOptions:
    account_name: str | None = "flutter_secure_storage_service"
    group_id: str | None = None
    accessibility: KeychainAccessibility | None = KeychainAccessibility.UNLOCKED
    synchronizable: bool = False
    label: str | None = None
    description: str | None = None
    comment: str | None = None
    is_invisible: bool | None = None
    is_negative: bool | None = None
    creation_date: datetime | None = None
    last_modified_date: datetime | None = None
    result_limit: int | None = None
    is_persistent: bool | None = None
    auth_ui_behavior: str | None = None
    access_control_flags: list[AccessControlFlag] = field(default_factory=list)


@dataclass
class IOSOptions(AppleOptions): ...


@dataclass
class MacOsOptions(AppleOptions):
    uses_data_protection_keychain: bool = True


@dataclass
class WebOptions:
    db_name: str = "FletEncryptedStorage"
    public_key: str = "FletSecureStorage"
    wrap_key: str = ""
    wrap_key_iv: str = ""
    use_session_storage: bool = False


@dataclass
class WindowsOptions:
    use_backward_compatibility: bool = False
