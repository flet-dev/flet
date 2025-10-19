from typing import Optional

import flet as ft
from flet_ads.base_ad import BaseAd
from flet_ads.types import PaidAdEvent


@ft.control("BannerAd")
class BannerAd(BaseAd):
    """
    Displays a banner ad.

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
