from dataclasses import dataclass
from enum import Enum
from typing import Optional

import flet as ft

__all__ = [
    "AdRequest",
    "NativeAdTemplateStyle",
    "NativeAdTemplateTextStyle",
    "NativeAdTemplateType",
    "NativeTemplateFontStyle",
    "PaidAdEvent",
    "PrecisionType",
]


class PrecisionType(Enum):
    UNKNOWN = "unknown"
    """An ad value with unknown precision."""

    ESTIMATED = "estimated"
    """An ad value estimated from aggregated data."""

    PUBLISHER_PROVIDED = "publisherProvided"
    """A publisher-provided ad value, such as manual CPMs in a mediation group."""

    PRECISE = "precise"
    """The precise value paid for this ad."""


@dataclass
class PaidAdEvent(ft.Event[ft.EventControlType]):
    """
    Event data for paid ad events.
    """

    value: float
    """
    The monetary value of the ad.
    """

    precision: PrecisionType
    """
    The precision of the ad value.
    """

    currency_code: str
    """
    The currency code of the ad value.
    """


@dataclass
class AdRequest:
    """
    Targeting info per the AdMob API.

    This class's properties mirror the native AdRequest API. See for example:
    [AdRequest.Builder for Android](https://developers.google.com/android/reference/com/google/android/gms/ads/AdRequest.Builder).
    """

    keywords: Optional[list[str]] = None
    """
    Words or phrases describing the current user activity.
    """

    content_url: Optional[str] = None
    """
    URL string for a webpage whose content matches the app’s primary content.

    This webpage content is used for targeting and brand safety purposes.
    """

    neighboring_content_urls: Optional[list[str]] = None
    """
    URLs representing web content near an ad.
    """

    non_personalized_ads: Optional[bool] = None
    """
    Non-personalized ads are ads that are not based on a user’s past behavior.

    For more information: https://support.google.com/admob/answer/7676680?hl=en
    """

    http_timeout: Optional[int] = None
    """
    A custom timeout (in milliseconds) for HTTPS calls during an ad request.

    Note:
        This is only supported in Android. (ignored on iOS)
    """

    extras: Optional[dict[str, str]] = None
    """
    Extras to pass to the AdMob adapter.
    """


class NativeAdTemplateType(Enum):
    SMALL = "small"
    MEDIUM = "medium"


class NativeTemplateFontStyle(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    MONOSPACE = "monospace"


@dataclass
class NativeAdTemplateTextStyle:
    size: Optional[ft.Number] = None
    text_color: Optional[ft.ColorValue] = None
    bgcolor: Optional[ft.ColorValue] = None
    style: Optional[NativeTemplateFontStyle] = None


@dataclass
class NativeAdTemplateStyle:
    template_type: NativeAdTemplateType = NativeAdTemplateType.MEDIUM
    main_bgcolor: Optional[ft.ColorValue] = None
    corner_radius: Optional[ft.Number] = None
    call_to_action_text_style: Optional[NativeAdTemplateTextStyle] = None
    primary_text_style: Optional[NativeAdTemplateTextStyle] = None
    secondary_text_style: Optional[NativeAdTemplateTextStyle] = None
    tertiary_text_style: Optional[NativeAdTemplateTextStyle] = None
