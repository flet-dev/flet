from typing import Optional

import flet as ft
from flet_ads.types import (
    ConsentRequestParameters,
    ConsentStatus,
    PrivacyOptionsRequirementStatus,
)

__all__ = ["ConsentManager"]


@ft.control("ConsentManager")
class ConsentManager(ft.Service):
    """
    Gathers and manages user consent for ads using
    Google's User Messaging Platform (UMP).

    Use this service to request consent information, present the consent form
    (for example, the GDPR/EEA consent dialog) and the privacy options form,
    and query the consent status before requesting ads.

    A typical flow looks like this:

    1. :meth:`request_consent_info_update` (at every app launch);
    2. :meth:`load_and_show_consent_form_if_required` (shows the form only if needed);
    3. :meth:`can_request_ads` (to decide whether to start loading ads).

    More info in the [AdMob documentation](https://developers.google.com/admob/flutter/privacy).

    Raises:
        FletUnsupportedPlatformException: When any of its methods are called on
            a web and/or non-mobile platform.
    """  # noqa: E501

    def init(self):
        super().init()
        if self.page.web or not self.page.platform.is_mobile():
            raise ft.FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on "
                f"Mobile (Android and iOS)"
            )

    async def request_consent_info_update(
        self, params: Optional[ConsentRequestParameters] = None
    ):
        """
        Requests an update of the user's consent information.

        This should be called (and awaited) at every app launch, before
        loading/showing a consent form or reading the consent status.

        Args:
            params: Parameters such as debug settings (useful for
                testing the form during development) or the under-age tag.
                If `None`, default parameters are used.
        """
        await self._invoke_method("request_consent_info_update", {"params": params})

    async def is_consent_form_available(self) -> bool:
        """
        Checks whether a consent form is available to be loaded and shown.

        Note:
            :meth:`request_consent_info_update` should be awaited before calling
            this method.

        Returns:
            `True` if a consent form is available, `False` otherwise.
        """
        return await self._invoke_method("is_consent_form_available")

    async def get_consent_status(self) -> ConsentStatus:
        """
        Get the user’s consent status.

        This value is cached between app sessions and can be read before
        requesting an update of the consent information.

        Returns:
            The user's current consent status.
        """
        return ConsentStatus(await self._invoke_method("get_consent_status"))

    async def can_request_ads(self) -> bool:
        """
        Indicates whether the app has gathered enough consent to request ads.

        Returns:
            `True` if ads can be requested, `False` otherwise.
        """
        return bool(await self._invoke_method("can_request_ads"))

    async def get_privacy_options_requirement_status(
        self,
    ) -> PrivacyOptionsRequirementStatus:
        """
        Gets the requirement status for showing a privacy options entry point.

        Returns:
            Whether a privacy options entry point (for example, a button
                that calls :meth:`show_privacy_options_form`) is required.
        """
        return PrivacyOptionsRequirementStatus(
            await self._invoke_method("get_privacy_options_requirement_status")
        )

    async def load_and_show_consent_form_if_required(self):
        """
        Loads a consent form and immediately shows it if consent is required.

        If consent is not required, this method completes without showing
        anything. This is the simplest way to gather consent: call
        :meth:`request_consent_info_update` first, then this method.
        """
        await self._invoke_method("load_and_show_consent_form_if_required")

    async def show_privacy_options_form(self):
        """
        Presents the privacy options form to the user.

        This lets users change or withdraw their consent after the initial
        choice. Only present it when :meth:`get_privacy_options_requirement_status`
        returns :attr:`flet_ads.PrivacyOptionsRequirementStatus.REQUIRED`.
        """
        await self._invoke_method("show_privacy_options_form")

    async def reset(self):
        """
        Resets the consent state.

        Warning:
            This is intended only for testing, allowing you to simulate a first-time
            user. It should not be used in production.
        """
        await self._invoke_method("reset")
