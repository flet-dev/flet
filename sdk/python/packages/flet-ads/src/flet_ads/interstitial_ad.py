import flet as ft
from flet_ads.base_ad import BaseAd


@ft.control("InterstitialAd")
class InterstitialAd(BaseAd):
    """
    Displays a full-screen interstitial ad.

    Raises:
        FletUnsupportedPlatformException: When using this control on a
            web and/or non-mobile platform.
    """

    async def show(self):
        """
        Present the loaded interstitial ad as a full-screen overlay.

        The ad must be loaded before this method is called.
        """

        await self._invoke_method("show")
