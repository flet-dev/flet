from typing import Optional

import flet as ft
from flet_permission_handler.types import Permission, PermissionStatus

__all__ = ["PermissionHandler"]


@ft.control("PermissionHandler")
class PermissionHandler(ft.Service):
    """
    Manages permissions for the application.

    Danger: Platform support
        Currently only supported on Android, iOS, Windows, and Web platforms.

    Raises:
        FletUnsupportedPlatformException: If the platform is not supported.
    """

    def before_update(self):
        super().before_update()

        # validate platform
        if not (
            self.page.web
            or self.page.platform
            in [
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.IOS,
                ft.PagePlatform.WINDOWS,
            ]
        ):
            raise ft.FletUnsupportedPlatformException(
                "PermissionHandler is currently only supported on Android, iOS, "
                "Windows, and Web platforms."
            )

    async def get_status(self, permission: Permission) -> Optional[PermissionStatus]:
        """
        Gets the current status of the given `permission`.

        Args:
            permission: The `Permission` to check the status for.

        Returns:
            A `PermissionStatus` if the status is known, otherwise `None`.
        """
        status = await self._invoke_method(
            method_name="get_status",
            arguments={"permission": permission},
        )
        return PermissionStatus(status) if status is not None else None

    async def request(self, permission: Permission) -> Optional[PermissionStatus]:
        """
        Request the user for access to the `permission` if access hasn't already been
        granted access before.

        Args:
            permission: The `Permission` to request.

        Returns:
            The new `PermissionStatus` after the request, or `None` if the request
                was not successful.
        """
        r = await self._invoke_method(
            method_name="request",
            arguments={"permission": permission},
        )
        return PermissionStatus(r) if r is not None else None

    async def open_app_settings(self) -> bool:
        """
        Opens the app settings page.

        Returns:
            `True` if the app settings page could be opened, otherwise `False`.
        """
        return await self._invoke_method(
            method_name="open_app_settings",
        )
