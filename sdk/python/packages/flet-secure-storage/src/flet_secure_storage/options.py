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
    """
    Specific options for Android platform for secure storage.

    Provides configurable options for encryption, key wrapping, biometric enforcement,
    and shared preferences naming.
    """

    reset_on_error: bool = False
    """
    When an error is detected, automatically reset all data to prevent fatal errors
    with unknown keys.

    Defaults to True. Be aware that data is PERMANENTLY erased when this occurs.
    """

    migrate_on_algorithm_change: bool = False
    """
    When the encryption algorithm changes, automatically migrate existing data
    to the new algorithm. Preserves data across algorithm upgrades.

    Defaults to True. If False, data may be lost when algorithm changes unless
    reset_on_error is True.
    """

    enforce_biometrics: bool = True
    """
    Whether to enforce biometric or PIN authentication.

    When True:
      - The plugin throws an exception if no biometric/PIN is enrolled.
      - The encryption key is generated with authentication required.

    When False (default):
      - The plugin gracefully degrades if biometrics are unavailable.
      - The key is generated without authentication required.

    Security note: set True for highly sensitive data.
    """

    key_cipher_algorithm: KeyCipherAlgorithm = KeyCipherAlgorithm.RSA_ECB_OAEP
    """
    Algorithm used to encrypt the secret key.

    Default: RSA/ECB/OAEPWithSHA-256AndMGF1Padding (API 23+).
    Legacy RSA/ECB/PKCS1Padding is available for backwards compatibility.
    """

    storage_cipher_algorithm: StorageCipherAlgorithm = StorageCipherAlgorithm.AES_GCM
    """
    Algorithm used to encrypt stored data.

    Default: AES/GCM/NoPadding (API 23+).
    Legacy AES/CBC/PKCS7Padding is available for backwards compatibility.
    """

    shared_preferences_name: str | None = None
    """
    The name of the shared preferences database to use.

    Default name will be used if not provided.
    Warning: changing this will prevent access to already saved preferences.
    """

    preferences_key_prefix: str | None = None
    """
    Prefix for shared preference keys. Ensures keys are unique to your app.

    An underscore (_) is added automatically. Changing this prevents access
    to existing preferences.
    """

    biometric_prompt_title: str = "Authenticate to access"
    """
    Title displayed in the biometric authentication prompt.
    """

    biometric_prompt_subtitle: str = "Use biometrics or device credentials"
    """
    Subtitle displayed in the biometric authentication prompt.
    """


@dataclass
class AppleOptions:
    """
    Specific options for Apple platforms (iOS/macOS) for secure storage.

    This class allows configuring keychain access and storage behavior.
    """

    account_name: str | None = "flutter_secure_storage_service"
    """
    Represents the service or application name associated with the item.

    Typically used to group related keychain items.
    """

    group_id: str | None = None
    """
    Specifies the app group for shared access. Allows multiple apps in the
    same app group to access the item.

    Note for macOS: Applies only if kSecUseDataProtectionKeychain or
    kSecAttrSynchronizable is set.
    """

    accessibility: KeychainAccessibility | None = KeychainAccessibility.UNLOCKED
    """
    Defines the accessibility level of the keychain item.

    Controls when the item is accessible (e.g., when device is unlocked
    or after first unlock).
    """

    synchronizable: bool = False
    """
    Indicates whether the keychain item should be synchronized with iCloud.
    True enables synchronization, False disables it.
    """
    label: str | None = None
    """
    A user-visible label for the keychain item.
    Helps identify the item in keychain management tools.
    """

    description: str | None = None
    """
    A description of the keychain item.
    Can describe a category of items (shared) or a specific item (unique).
    """

    comment: str | None = None
    """
    A comment associated with the keychain item.
    Often used for metadata or debugging information.
    """

    is_invisible: bool | None = None
    """
    Indicates whether the keychain item is hidden from user-visible lists.
    Can apply to all items in a category (shared) or specific items (unique).
    """

    is_negative: bool | None = None
    """
    Indicates whether the item is a placeholder or a negative entry.
    Typically unique to individual keychain items.
    """

    creation_date: datetime | None = None
    """
    The creation date of the keychain item.
    Automatically set by the system when an item is created.
    """

    last_modified_date: datetime | None = None
    """
    The last modification date of the keychain item.
    Automatically updated when an item is modified.
    """

    result_limit: int | None = None
    """
    Specifies the maximum number of results to return in a query.
    For example, 1 for a single result, or all for all matching results.
    """

    is_persistent: bool | None = None
    """
    Indicates whether to return a persistent reference to the keychain item.
    Used for persistent access across app sessions.
    """

    auth_ui_behavior: str | None = None
    """
    Controls how authentication UI is presented during secure operations.
    Determines whether authentication prompts are displayed to the user.
    """

    access_control_flags: list[AccessControlFlag] = field(default_factory=list)
    """
    Keychain access control flags that define security conditions for accessing items.

    Rules for combining flags:
      - Use AccessControlFlag.OR to allow access if any condition is met.
      - Use AccessControlFlag.AND to require that all specified conditions are met.
      - Only one logical operator (or/and) can be used per combination.

    Supported flags:
      - USER_PRESENCE: Requires user authentication via biometrics or passcode.
      - BIOMETRY_ANY: Allows access with any enrolled biometrics.
      - BIOMETRY_CURRENT_SET: Requires currently enrolled biometrics.
      - DEVICE_PASSCODE: Requires device passcode authentication.
      - WATCH: Allows access with a paired Apple Watch.
      - PRIVATE_KEY_USAGE: Enables use of a private key for signing operations.
      - APPLICATION_PASSWORD: Uses an app-defined password for encryption.
    """


@dataclass
class IOSOptions(AppleOptions):
    """
    Specific options for iOS platform.

    Currently, there are no iOS-specific options available.
    All configurable options are inherited from AppleOptions.
    """


@dataclass
class MacOsOptions(AppleOptions):
    """
    Specific options for macOS platform.
    Extends `AppleOptions` and adds the `usesDataProtectionKeychain` parameter.
    """

    uses_data_protection_keychain: bool = True
    """
    Indicates whether the macOS data protection keychain is used.
    Not applicable on iOS.
    """


@dataclass
class WebOptions:
    """
    Specific options for the Web platform for secure storage.

    Configures database, encryption, and storage behavior on web platforms.
    """

    db_name: str = "FletEncryptedStorage"
    """
    The name of the database used for secure storage.
    Defaults to 'FlutterEncryptedStorage'.
    """

    public_key: str = "FletSecureStorage"
    """
    The public key used for encryption.
    Defaults to 'FlutterSecureStorage'.
    """

    wrap_key: str = ""
    """
    The key used to wrap the encryption key.
    """

    wrap_key_iv: str = ""
    """
    The initialization vector (IV) used for the wrap key.
    """

    use_session_storage: bool = False
    """
    Whether to use session storage instead of local storage.
    Defaults to False.
    """


@dataclass
class WindowsOptions:
    """
    Specific options for Windows platform for secure storage.

    Allows configuring backward compatibility when reading/writing
    values from previous versions of storage.
    """

    use_backward_compatibility: bool = False
    """
    If True, attempts to read values written by previous versions of the storage.
    When reading or writing old storage values, they will be automatically
    migrated to new storage.

    Notes:
      - May introduce performance overhead.
      - May cause errors for keys containing `"`, `<`, `>`, `|`, `:`, `*`, `?`, `/`, `\`
      or any ASCII control characters.
      - May cause errors for keys containing `/../`, `\..\`, or similar patterns.
      - May cause errors for very long keys (length depends on app's product name,
        company name, and executing account).

    Default: False.

    Example:
        storage = SecureStorage()
        await storage.get_all(WindowsOptions(use_backward_compatibility=True))
    """
