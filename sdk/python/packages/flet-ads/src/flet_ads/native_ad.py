import flet as ft
from flet_ads.banner_ad import BannerAd
from flet_ads.types import NativeAdTemplateStyle

__all__ = ["NativeAd"]


@ft.control("NativeAd")
class NativeAd(BannerAd):
    """
    Renders a native ad.
    """

    factory_id: str = None
    """
    An identifier for the factory that creates the Platform view.

    Raises:
        ValueError: When neither `factory_id` nor [`template_style`][(c).] is set.
    """

    template_style: NativeAdTemplateStyle = None
    """
    A style for the native ad template.

    Raises:
        ValueError: When neither [`factory_id`][(c).] nor `template_style` is set.
    """

    def before_update(self):
        super().before_update()
        if self.factory_id is None and self.template_style is None:
            raise ValueError("factory_id or template_style must be set")
