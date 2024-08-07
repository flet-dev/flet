from typing import Any, Optional
import json

# import warnings
from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import PagePlatform
from .mac_authentication import MacLocalAuth
from .linux_authentication import LinuxLocalAuth


class LocalAuthentication(Control):
    """
    A control to use native authentication. Works on iOS, Android, Windows, MacOS, Linux. Based on local_auth Flutter widget (https://pub.dev/packages/local_auth).
    LocalAuthentication control is non-visual and should be added to `page.overlay` list.
    Example:
    ```
    import flet as ft
    def main(page: ft.Page):
        auth = ft.LocalAuthentication()
        def on_click(e):
            print(
                auth.authenticate(
                    title="title", biometricsOnly=False
                )
            )
        page.overlay.append(auth)
        page.add(ft.SafeArea(content=ft.TextButton(text="authenticate", on_click=on_click)))
    ft.app(main)
    ```
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "localauthentication"

    def before_update(self):
        super().before_update()
        # Both macOS and Linux have platform dependant dependencies.
        # Hence initiating MacLocalAuth and LinuxLocalAuth after checking the platform
        if self.page.platform == PagePlatform.MACOS:
            self.mac_local_auth = MacLocalAuth()
        elif self.page.platform == PagePlatform.LINUX:
            self.linux_local_auth = LinuxLocalAuth()

    def available(self, wait_timeout: Optional[int] = 5) -> bool:
        if self.page.platform == PagePlatform.MACOS:
            sr = self.mac_local_auth.is_available()
        elif self.page.platform == PagePlatform.LINUX:
            # linux always has a user with password.
            # Even if not so, a popup asking to authenticate without asking password will be shown
            sr = True
        else:
            sr = (
                self.invoke_method(
                    "available", wait_for_result=True, wait_timeout=wait_timeout
                )
                == "true"
            )
        # print(json.loads(sr))
        # if sr_json["error"] != "null":

        return sr

    async def available_async(self, wait_timeout: Optional[int] = 5) -> bool:
        if self.page.platform == PagePlatform.MACOS:
            sr = await self.mac_local_auth.is_available()
        elif self.page.platform == PagePlatform.LINUX:
            # linux always has a user with password.
            # Even if not so, a popup asking to authenticate without asking password will be shown
            sr = True
        else:
            sr = (
                await self.invoke_method_async(
                    "available", wait_for_result=True, wait_timeout=wait_timeout
                )
                == "true"
            )

        return sr

    def authenticate(
        self,
        reason: Optional[str],
        biometrics_only: bool = False,
        use_error_dialogs: bool = True,
        sensitive_transaction: bool = True,
        wait_timeout: Optional[int] = 60,
    ) -> bool:
        if self.page.platform == PagePlatform.MACOS:
            sr = self.mac_local_auth.authenticate_mac(reason)
        elif self.page.platform == PagePlatform.LINUX:
            sr = self.linux_local_auth.authenticate_linux()
        else:
            sr = self.invoke_method(
                "authenticate",
                wait_for_result=True,
                wait_timeout=wait_timeout,
                arguments={
                    "title": reason,
                    "biometricsOnly": str(biometrics_only).lower(),
                    "useErrorDialogs": str(use_error_dialogs).lower(),
                    "sensitiveTransaction": str(sensitive_transaction).lower(),
                },
            )
            sr = json.loads(sr)

        return sr

    async def authenticate_async(
        self,
        reason: Optional[str],
        biometrics_only: bool = False,
        use_error_dialogs: bool = True,
        sensitive_transaction: bool = True,
        wait_timeout: Optional[int] = 60,
    ) -> bool:
        if self.page.platform == PagePlatform.MACOS:
            sr = self.mac_local_auth.authenticate_mac(reason)
        elif self.page.platform == PagePlatform.LINUX:
            sr = self.linux_local_auth.authenticate_linux()
        else:
            sr = await self.invoke_method_async(
                "authenticate",
                wait_for_result=True,
                wait_timeout=wait_timeout,
                arguments={
                    "title": reason,
                    "biometricsOnly": str(biometrics_only).lower(),
                    "useErrorDialogs": str(use_error_dialogs).lower(),
                    "sensitiveTransaction": str(sensitive_transaction).lower(),
                },
            )

            sr_json = json.loads(sr)

        return sr_json
