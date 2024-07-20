from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref
import json


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

        self.turned_on = False

    def _get_control_name(self):
        return "localauthentication"

    def supported(self, wait_timeout: Optional[int] = 5) -> dict:
        sr = self.invoke_method(
            "supported", wait_for_result=True, wait_timeout=wait_timeout
        )

        sr = sr.split(",")
        biometrics = sr[0].split(" ")[1]
        weak = sr[1].split(" ")[1]
        strong = sr[2].split(" ")[1]
        devicesupport = sr[3].split(" ")[1]
        data = {
            "biometrics": True if biometrics == "true" else False,
            "weak": True if weak == "true" else False,
            "strong": True if strong == "true" else False,
            "devicesupport": True if devicesupport == "true" else False,
        }

        return data

    async def supported_async(self, wait_timeout: Optional[int] = 5) -> dict:
        sr = await self.invoke_method_async(
            "supported", wait_for_result=True, wait_timeout=wait_timeout
        )

        sr.split(",")

        biometrics = sr[0].split(" ")[1]
        weak = sr[1].split(" ")[1]
        strong = sr[2].split(" ")[1]
        devicesupport = sr[3].split(" ")[1]
        data = {
            "biometrics": True if biometrics == "true" else False,
            "weak": True if weak == "true" else False,
            "strong": True if strong == "true" else False,
            "devicesupport": True if devicesupport == "true" else False,
        }

        return data

    def authenticate(
        self,
        title: str,
        biometricsOnly: bool = False,
        useErrorDialogs: bool = False,
        wait_timeout: Optional[int] = 60,
    ) -> bool:
        sr = self.invoke_method(
            "authenticate",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            arguments={
                "title": title,
                "biometricsOnly": str(biometricsOnly).lower(),
                "useErrorDialogs": str(useErrorDialogs).lower(),
            },
        )

        return True if sr == "true" else False

    async def authenticate_async(
        self,
        title: str,
        biometricsOnly: bool = False,
        useErrorDialogs: bool = False,
        wait_timeout: Optional[int] = 60,
    ) -> bool:
        sr = await self.invoke_method_async(
            "authenticate",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            arguments={
                "title": title,
                "biometricsOnly": str(biometricsOnly).lower(),
                "useErrorDialogs": str(useErrorDialogs).lower(),
            },
        )

        return True if sr == "true" else False
