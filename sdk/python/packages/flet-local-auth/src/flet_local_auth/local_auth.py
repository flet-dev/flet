from typing import Optional

import flet as ft
from flet.controls.base_control import control
from flet.controls.services.service import Service

from flet_local_auth.types import (
    AndroidAuthMessages,
    BiometricType,
    IOSAuthMessages,
    LocalAuthErrorCode,
    LocalAuthException,
    WindowsAuthMessages,
)

__all__ = [
    "AndroidAuthMessages",
    "BiometricType",
    "IOSAuthMessages",
    "LocalAuthErrorCode",
    "LocalAuthentication",
    "LocalAuthException",
    "WindowsAuthMessages",
]


@control("LocalAuthentication")
class LocalAuthentication(Service):
    """
    Authenticates the user with on-device biometrics or device credentials.

    Danger: Platform support
        Supported on Android, iOS, macOS, and Windows. Not supported on Linux or Web.

    Raises:
        FletUnsupportedPlatformException: If the platform is not supported.
        LocalAuthException: If authentication fails.
    """

    def before_update(self):
        super().before_update()

        if self.page.web or self.page.platform == ft.PagePlatform.LINUX:
            raise ft.FletUnsupportedPlatformException(
                "LocalAuthentication is not supported on Linux or Web platforms."
            )

    async def is_device_supported(self) -> bool:
        """
        Returns whether the device can authenticate with biometrics or credentials.
        """
        return await self._invoke_method("is_device_supported")

    async def can_check_biometrics(self) -> bool:
        """
        Returns whether the device has biometric hardware available.
        """
        return await self._invoke_method("can_check_biometrics")

    async def get_available_biometrics(self) -> list[BiometricType]:
        """
        Returns the biometrics currently enrolled on the device.
        """
        result = await self._invoke_method("get_available_biometrics")
        return [BiometricType(value) for value in result or []]

    async def authenticate(
        self,
        reason: str,
        *,
        biometric_only: bool = False,
        sensitive_transaction: bool = True,
        persist_across_backgrounding: bool = False,
        android_messages: Optional[AndroidAuthMessages] = None,
        ios_messages: Optional[IOSAuthMessages] = None,
        windows_messages: Optional[WindowsAuthMessages] = None,
    ) -> bool:
        """
        Prompts the user to authenticate locally.

        Args:
            reason: The message shown in the system authentication dialog.
            biometric_only: Whether to allow only biometric authentication.
            sensitive_transaction: Whether to treat the transaction as sensitive.
            persist_across_backgrounding: Whether to retry after the app is
                foregrounded again if authentication was interrupted.
            android_messages: Optional Android dialog customization.
            ios_messages: Optional iOS dialog customization.
            windows_messages: Optional Windows dialog customization.

        Returns:
            `True` when authentication succeeds.

        Raises:
            LocalAuthException: If authentication fails or is canceled.
        """
        result = await self._invoke_method(
            method_name="authenticate",
            arguments={
                "reason": reason,
                "biometric_only": biometric_only,
                "sensitive_transaction": sensitive_transaction,
                "persist_across_backgrounding": persist_across_backgrounding,
                "android_messages": android_messages,
                "ios_messages": ios_messages,
                "windows_messages": windows_messages,
            },
        )
        self._raise_for_error(result)
        return bool(result)

    async def stop_authentication(self) -> bool:
        """
        Cancels any in-progress authentication prompt.

        Returns:
            `True` if authentication was canceled successfully.
        """
        return await self._invoke_method("stop_authentication")

    @staticmethod
    def _raise_for_error(result: object) -> None:
        if not isinstance(result, dict) or "error_code" not in result:
            return

        code_value = result.get("error_code")
        try:
            code = LocalAuthErrorCode(code_value)
        except ValueError:
            code = LocalAuthErrorCode.UNKNOWN_ERROR

        raise LocalAuthException(
            code=code,
            description=result.get("error_description"),
        )
