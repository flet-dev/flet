from typing import Optional

import flet as ft
from flet_ads.base_ad import BaseAd
from flet_ads.types import PaidAdEvent


@ft.control("BannerAd")
class BannerAd(BaseAd):
    """
    Displays a banner ad.

    Example: Test IDs
        AdMob [provides](https://developers.google.com/admob/flutter/banner#always_test_with_test_ads)
        unit IDs for testing purposes. Set [`unit_id`][(c).] to the appropriate value
        based on the platform you're testing on:

        - Android: `"ca-app-pub-3940256099942544/9214589741"`
        - iOS: `"ca-app-pub-3940256099942544/2435281174"`

        Remember to replace them in production.

    Raises:
        FletUnsupportedPlatformException: When this control is used on a web
            and/or non-mobile platform.
    """

    on_will_dismiss: Optional[ft.ControlEventHandler["BannerAd"]] = None
    """
    Called before dismissing a full screen view.

    Note:
        Only available on iOS.
    """

    on_paid: Optional[ft.ControlEventHandler[PaidAdEvent["BannerAd"]]] = None
    """
    Called when this ad is estimated to have earned money.

    Available for allowlisted accounts only.
    """
