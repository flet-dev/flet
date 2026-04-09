import flet as ft
from flet_ads.base_ad import BaseAd


@ft.control("InterstitialAd")
class InterstitialAd(ft.Service, BaseAd):
    """
    Displays a full-screen interstitial ad.

    Note:
        Each instance is allowed to be shown (using :meth:`show`) only once.
        To show another ad, create a new instance. Reusing an already-shown instance
        will result in errors or unexpected behavior.

    Example: Test IDs
        AdMob [provides](https://developers.google.com/admob/flutter/banner#always_test_with_test_ads)
        unit IDs for testing purposes. Set :attr:`~flet_ads.BaseAd.unit_id`
        to the appropriate value based on the platform you're testing on:

        - Android: `"ca-app-pub-3940256099942544/1033173712"`
        - iOS: `"ca-app-pub-3940256099942544/4411468910"`

        Remember to replace them in production.

    Raises:
        FletUnsupportedPlatformException: When using this control on a
            web and/or non-mobile platform.
    """  # noqa: E501

    async def show(self):
        """
        Present the loaded interstitial ad as a full-screen overlay.

        The ad must be loaded before this method is called.
        """

        await self._invoke_method("show")
