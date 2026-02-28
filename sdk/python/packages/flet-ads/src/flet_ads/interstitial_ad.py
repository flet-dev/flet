from dataclasses import field
from typing import Optional

import flet as ft
from flet_ads.types import AdRequest


@ft.control("InterstitialAd")
class InterstitialAd(ft.Service):
    """
    Displays a full-screen interstitial ad.

    This is a non-visual control and should be added to
    [`Page.services`][flet.].

    Raises:
        FletUnsupportedPlatformException: When using this control on a
            web and/or non-mobile platform.
    """

    unit_id: str
    """
    Ad unit ID for this ad.
    """

    request: AdRequest = field(default_factory=lambda: AdRequest())
    """
    Targeting information used to fetch an Ad.
    """

    on_load: Optional[ft.ControlEventHandler["InterstitialAd"]] = None
    """
    Called when this ad is loaded successfully.
    """

    on_error: Optional[ft.ControlEventHandler["InterstitialAd"]] = None
    """
    Called when an ad request failed.

    Event handler argument [`data`][flet.Event.data] property
    contains information about the error.
    """

    on_open: Optional[ft.ControlEventHandler["InterstitialAd"]] = None
    """
    Called when this ad opens up.

    A full screen view/overlay is presented in response to the user clicking
    on an ad. You may want to pause animations and time sensitive
    interactions.
    """

    on_close: Optional[ft.ControlEventHandler["InterstitialAd"]] = None
    """
    Called when the full screen view has been closed.

    You should restart anything paused while handling [`on_open`][(c).].
    """

    on_impression: Optional[ft.ControlEventHandler["InterstitialAd"]] = None
    """
    Called when an impression occurs on this ad.
    """

    on_click: Optional[ft.ControlEventHandler["InterstitialAd"]] = None
    """
    Called when this ad is clicked.
    """

    def before_update(self):
        if self.page.web or not self.page.platform.is_mobile():
            raise ft.FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on "
                f"Mobile (Android and iOS)"
            )

    async def show(self):
        """
        Present the loaded interstitial ad as a full-screen overlay.

        The ad must be loaded before this method is called.
        """

        await self._invoke_method("show")
