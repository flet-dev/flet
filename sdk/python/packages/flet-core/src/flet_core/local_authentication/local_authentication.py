from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import PagePlatform
from .mac_authentication import is_available, authenticate_mac


class LocalAuthentication(Control):
    """
    A control to use native authentication. Works on iOS, Android and Windows. Based on local_auth Flutter widget (https://pub.dev/packages/local_auth).
    LocalAuthentication control is non-visual and should be added to `page.overlay` list.
    Example:
    ```
    import flet as ft
    def main(page: ft.Page):
        auth = ft.LocalAuthentication()
        def on_click(e):
            print(
                auth.authenticate(
                    title="title", biometricsOnly=False, useErrorDialogs=True
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
        self.platform = self.page.platform
        return super().before_update()

    def available(self, wait_timeout: Optional[int] = 5) -> dict:
        if self.platform == PagePlatform.MACOS:
            sr = is_available()
        elif self.platform == PagePlatform.LINUX:
            return False
        else:
            sr = (
                self.invoke_method(
                    "available", wait_for_result=True, wait_timeout=wait_timeout
                )
                == "true"
            )

        return sr

    async def available_async(self, wait_timeout: Optional[int] = 5) -> dict:
        if self.platform == PagePlatform.MACOS:
            sr = await is_available()
        elif self.platform == PagePlatform.LINUX:
            return False
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
        title: str,
        biometricsOnly: bool = False,
        wait_timeout: Optional[int] = 60,
    ) -> bool:
        if self.platform == PagePlatform.MACOS:
            sr = authenticate_mac(title)
        if self.platform == PagePlatform.LINUX:
            return False
        else:
            sr = (
                self.invoke_method(
                    "authenticate",
                    wait_for_result=True,
                    wait_timeout=wait_timeout,
                    arguments={
                        "title": title,
                        "biometricsOnly": str(biometricsOnly).lower(),
                    },
                )
                == "true"
            )

        return sr

    async def authenticate_async(
        self,
        title: str,
        biometricsOnly: bool = False,
        wait_timeout: Optional[int] = 60,
    ) -> bool:
        if not self.is_macos:
            sr = await self.invoke_method_async(
                "authenticate",
                wait_for_result=True,
                wait_timeout=wait_timeout,
                arguments={
                    "title": title,
                    "biometricsOnly": str(biometricsOnly).lower(),
                },
            )
            sr = sr == "true"
        elif self.platform == PagePlatform.LINUX:
            return False
        else:
            sr = await authenticate_mac(title)

        return sr
