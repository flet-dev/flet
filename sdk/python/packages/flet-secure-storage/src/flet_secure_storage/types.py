from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class KeychainAccessibility(Enum):
    """
    KeyChain accessibility attributes for iOS/macOS platforms.

    These attributes determine when the app can access secure values
    stored in the Keychain.
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

    Items with this attribute do not migrate to a new device.
    """

    FIRST_UNLOCK = "first_unlock"
    """
    The data in the keychain item cannot be accessed after a restart until
    the device has been unlocked once by the user.

    Enables access to secure values after the device is unlocked for the first
    time after a reboot.
    """

    FIRST_UNLOCK_THIS_DEVICE = "first_unlock_this_device"
    """
    The data in the keychain item cannot be accessed after
    a restart until the device has been unlocked once by the user.

    Items with this attribute do not migrate to a new device.

    Allows access to secure values only after the device is unlocked for the first time
    since installation on this device.
    """


class AccessControlFlag(Enum):
    """
    Keychain access control flags that define security conditions for accessing items.

    These flags can be combined to create complex access control policies using
    the `access_control_flags` parameter in `IOSOptions` or `MacOsOptions`.

    Rules for combining flags:
        - Use `AccessControlFlag.OR` to allow access if any condition is met
        - Use `AccessControlFlag.AND` to require that all specified conditions are met
        - Only one logical operator (OR/AND) can be used per combination
    """

    DEVICE_PASSCODE = "devicePasscode"
    """
    Constraint to access an item with a passcode.
    """

    BIOMETRY_ANY = "biometryAny"
    """
    Constraint to access an item with biometrics (Touch ID/Face ID).
    """

    BIOMETRY_CURRENT_SET = "biometryCurrentSet"
    """
    Constraint to access an item with the currently enrolled biometrics.
    """

    USER_PRESENCE = "userPresence"
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

    APPLICATION_PASSWORD = "applicationPassword"
    """
    Use an application-provided password for encryption.
    """

    PRIVATE_KEY_USAGE = "privateKeyUsage"
    """
    Enable private key usage for signing operations.
    """


class KeyCipherAlgorithm(Enum):
    """
    Algorithm used to encrypt/wrap the secret key in Android KeyStore.

    Different algorithms provide different security guarantees and compatibility levels:

    - RSA algorithms wrap the AES encryption key with RSA (no biometric support)
    - AES algorithm stores the key directly in Android KeyStore
    (supports biometric authentication)

    See the [AndroidOptions] class for usage examples and combinations.
    """

    RSA_ECB_PKCS1_PADDING = "RSA_ECB_PKCS1Padding"
    """
    Legacy RSA/ECB/PKCS1Padding for backwards compatibility.
    """

    RSA_ECB_OAEP_WITH_SHA256_AND_MGF1_PADDING = "RSA_ECB_OAEPwithSHA_256andMGF1Padding"
    """
    RSA/ECB/OAEPWithSHA-256AndMGF1Padding (API 23+).

    This is the default and recommended algorithm for most use cases.
    Provides strong authenticated encryption without biometrics.
    """

    AES_GCM_NO_PADDING = "AES_GCM_NoPadding"
    """
    AES/GCM/NoPadding for KeyStore-based key wrapping (supports biometrics).

    Use this algorithm when you need biometric authentication support.
    Requires API 23+ for basic use, API 28+ for enforced biometric authentication.
    """


class StorageCipherAlgorithm(Enum):
    """
    Algorithm used to encrypt stored data on Android.

    Modern applications should use `AES_GCM_NO_PADDING` for better security.
    The legacy `AES_CBC_PKCS7_PADDING` is provided for backwards compatibility only.
    """

    AES_CBC_PKCS7_PADDING = "AES_CBC_PKCS7Padding"
    """
    Legacy AES/CBC/PKCS7Padding for backwards compatibility.
    """

    AES_GCM_NO_PADDING = "AES_GCM_NoPadding"
    """
    AES/GCM/NoPadding (API 23+).

    This is the default and recommended storage cipher algorithm.
    Provides authenticated encryption with associated data (AEAD).
    """


@dataclass
class AndroidOptions:
    """
    Specific options for Android platform for secure storage.

    Provides configurable options for encryption, key wrapping, biometric enforcement,
    and shared preferences naming.
    """

    reset_on_error: bool = True
    """
    When an error is detected, automatically reset all data to prevent fatal errors
    with unknown keys.

    Be aware that data is PERMANENTLY erased when this occurs.
    """

    migrate_on_algorithm_change: bool = True
    """
    When the encryption algorithm changes, automatically migrate existing data
    to the new algorithm. Preserves data across algorithm upgrades.

    If False, data may be lost when algorithm changes unless
    reset_on_error is True.
    """

    enforce_biometrics: bool = False
    """
    Whether to enforce biometric or PIN authentication.

    When True:
      - The plugin throws an exception if no biometric/PIN is enrolled.
      - The encryption key is generated with authentication required.

    When False:
      - The plugin gracefully degrades if biometrics are unavailable.
      - The key is generated without authentication required.
    """

    key_cipher_algorithm: KeyCipherAlgorithm = (
        KeyCipherAlgorithm.RSA_ECB_OAEP_WITH_SHA256_AND_MGF1_PADDING
    )
    """
    Algorithm used to encrypt the secret key.

    Legacy RSA/ECB/PKCS1Padding is available for backwards compatibility.
    """

    storage_cipher_algorithm: StorageCipherAlgorithm = (
        StorageCipherAlgorithm.AES_GCM_NO_PADDING
    )
    """
    Algorithm used to encrypt stored data.

    Legacy AES/CBC/PKCS7Padding is available for backwards compatibility.
    """

    shared_preferences_name: Optional[str] = None
    """
    The name of the shared preferences database to use.

    Changing this will prevent access to already saved preferences.
    """

    preferences_key_prefix: Optional[str] = None
    """
    Prefix for shared preference keys. Ensures keys are unique to your app.

    An underscore (_) is added automatically.

    Changing this prevents access to existing preferences.
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
    Use `IOSOptions` for iOS-specific configuration
    or `MacOsOptions` for macOS-specific configuration.

    Note:
        - Most options apply to both iOS and macOS
        - Some options (like `group_id` on macOS) only apply when
        certain keychain flags are set
        - See individual option documentation for platform-specific behavior
    """

    account_name: Optional[str] = "flet_secure_storage_service"
    """
    Represents the service or application name associated with the item.

    Typically used to group related keychain items.
    """

    group_id: Optional[str] = None
    """
    Specifies the app group for shared access. Allows multiple apps in the
    same app group to access the item.
    """

    accessibility: Optional[KeychainAccessibility] = KeychainAccessibility.UNLOCKED
    """
    Defines the accessibility level of the keychain item.

    Controls when the item is accessible (e.g., when device is unlocked
    or after first unlock).
    """

    synchronizable: bool = False
    """
    Indicates whether the keychain item should be synchronized with iCloud.

    - True: Enables synchronization across user's devices
    - False: Item stays local to this device only
    """

    label: Optional[str] = None
    """
    A user-visible label for the keychain item.
    Helps identify the item in keychain management tools.
    """

    description: Optional[str] = None
    """
    A description of the keychain item.
    Can describe a category of items (shared) or a specific item (unique).
    """

    comment: Optional[str] = None
    """
    A comment associated with the keychain item.
    Often used for metadata or debugging information.
    """

    invisible: Optional[bool] = None
    """
    Indicates whether the keychain item is hidden from user-visible lists.
    Can apply to all items in a category (shared) or specific items (unique).
    """

    is_negative: Optional[bool] = None
    """
    Indicates whether the item is a placeholder or a negative entry.
    Typically unique to individual keychain items.
    """

    creation_date: Optional[datetime] = None
    """
    The creation date of the keychain item.
    Automatically set by the system when an item is created.
    """

    last_modified_date: Optional[datetime] = None
    """
    The last modification date of the keychain item.
    Automatically updated when an item is modified.
    """

    result_limit: Optional[int] = None
    """
    Specifies the maximum number of results to return in a query.
    For example, 1 for a single result, or `None` for all matching results.
    """

    is_persistent: Optional[bool] = None
    """
    Indicates whether to return a persistent reference to the keychain item.
    Used for persistent access across app sessions.
    """

    auth_ui_behavior: Optional[str] = None
    """
    Controls how authentication UI is presented during secure operations.
    Determines whether authentication prompts are displayed to the user.
    """

    access_control_flags: list[AccessControlFlag] = field(default_factory=list)
    """
    Keychain access control flags that define security conditions for accessing items.
    """


@dataclass
class IOSOptions(AppleOptions):
    """
    iOS-specific configuration for secure storage.

    All configurable options are inherited from `AppleOptions`.
    There are currently no iOS-only options.
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
    """

    public_key: str = "FletSecureStorage"
    """
    The public key used for encryption.
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
    """


@dataclass
class WindowsOptions:
    """
    Specific options for Windows platform for secure storage.

    Allows configuring backward compatibility when reading/writing
    values from previous versions of storage.

    Note:
        You need the C++ ATL libraries installed along with Visual Studio Build Tools.
        Download from: https://visualstudio.microsoft.com/downloads/?q=build+tools
        Make sure the C++ ATL under optional components is installed as well.
    """

    use_backward_compatibility: bool = False
    """
    If True, attempts to read values written by previous versions of the storage.
    When reading or writing old storage values, they will be automatically
    migrated to new storage.

    Note:
      - May introduce performance overhead.
      - May cause errors for keys with `"`, `<`, `>`, `|`, `:`, `*`, `?`, `/`, `\\`.
      or any ASCII control characters.
      - May cause errors for keys containing `/../`, `\\..\\`, or similar patterns.
      - May cause errors for very long keys (length depends on app's product name,
        company name, and executing account).
    """
