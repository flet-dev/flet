from enum import Enum
from typing import Optional

import flet as ft


class BiometricType(Enum):
    """
    Biometric types reported by the device.
    """

    FACE = "face"
    FINGERPRINT = "fingerprint"
    WEAK = "weak"
    STRONG = "strong"


class LocalAuthErrorCode(Enum):
    """
    Error codes reported by local authentication failures.
    """

    AUTH_IN_PROGRESS = "authInProgress"
    UI_UNAVAILABLE = "uiUnavailable"
    USER_CANCELED = "userCanceled"
    TIMEOUT = "timeout"
    SYSTEM_CANCELED = "systemCanceled"
    NO_CREDENTIALS_SET = "noCredentialsSet"
    NO_BIOMETRICS_ENROLLED = "noBiometricsEnrolled"
    NO_BIOMETRIC_HARDWARE = "noBiometricHardware"
    BIOMETRIC_HARDWARE_TEMPORARILY_UNAVAILABLE = (
        "biometricHardwareTemporarilyUnavailable"
    )
    TEMPORARY_LOCKOUT = "temporaryLockout"
    BIOMETRIC_LOCKOUT = "biometricLockout"
    USER_REQUESTED_FALLBACK = "userRequestedFallback"
    DEVICE_ERROR = "deviceError"
    UNKNOWN_ERROR = "unknownError"


@ft.value
class AndroidAuthMessages:
    """
    Customizable Android authentication dialog strings.
    """

    sign_in_title: Optional[str] = None
    cancel_button: Optional[str] = None
    device_credentials_required_title: Optional[str] = None
    device_credentials_setup_description: Optional[str] = None
    go_to_settings_button: Optional[str] = None
    go_to_settings_description: Optional[str] = None
    biometric_hint: Optional[str] = None
    biometric_not_recognized: Optional[str] = None
    biometric_success: Optional[str] = None
    biometric_required_title: Optional[str] = None


@ft.value
class IOSAuthMessages:
    """
    Customizable iOS authentication dialog strings.
    """

    cancel_button: Optional[str] = None
    go_to_settings_button: Optional[str] = None
    go_to_settings_description: Optional[str] = None
    lock_out: Optional[str] = None
    localized_fallback_title: Optional[str] = None


@ft.value
class WindowsAuthMessages:
    """
    Customizable Windows authentication dialog strings.
    """

    sign_in_title: Optional[str] = None
    cancel_button: Optional[str] = None


class LocalAuthException(ft.FletException):
    """
    Raised when local authentication fails.
    """

    def __init__(
        self,
        code: LocalAuthErrorCode,
        description: Optional[str] = None,
    ):
        self.code = code
        self.description = description
        message = description or code.value
        super().__init__(message)
