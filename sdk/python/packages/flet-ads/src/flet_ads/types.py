from dataclasses import dataclass
from enum import Enum
from typing import Optional

import flet as ft

__all__ = [
    "AdRequest",
    "ConsentDebugSettings",
    "ConsentRequestParameters",
    "ConsentStatus",
    "DebugGeography",
    "NativeAdTemplateStyle",
    "NativeAdTemplateTextStyle",
    "NativeAdTemplateType",
    "NativeTemplateFontStyle",
    "PaidAdEvent",
    "PrecisionType",
    "PrivacyOptionsRequirementStatus",
]


class PrecisionType(Enum):
    """Describes how accurately a paid ad value is reported."""

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


@ft.value
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


@ft.value
class NativeAdTemplateTextStyle:
    size: Optional[ft.Number] = None
    text_color: Optional[ft.ColorValue] = None
    bgcolor: Optional[ft.ColorValue] = None
    style: Optional[NativeTemplateFontStyle] = None


@ft.value
class NativeAdTemplateStyle:
    template_type: NativeAdTemplateType = NativeAdTemplateType.MEDIUM
    main_bgcolor: Optional[ft.ColorValue] = None
    corner_radius: Optional[ft.Number] = None
    call_to_action_text_style: Optional[NativeAdTemplateTextStyle] = None
    primary_text_style: Optional[NativeAdTemplateTextStyle] = None
    secondary_text_style: Optional[NativeAdTemplateTextStyle] = None
    tertiary_text_style: Optional[NativeAdTemplateTextStyle] = None


class ConsentStatus(Enum):
    """
    User consent status, as reported by the User Messaging Platform (UMP).
    """

    NOT_REQUIRED = "notRequired"
    """User consent is not required."""

    OBTAINED = "obtained"
    """User consent has been obtained."""

    REQUIRED = "required"
    """User consent is required but has not yet been obtained."""

    UNKNOWN = "unknown"
    """Consent status is unknown."""


class PrivacyOptionsRequirementStatus(Enum):
    """
    Whether a privacy options entry point (e.g. a button that
    re-opens the privacy options form) is required.
    """

    NOT_REQUIRED = "notRequired"
    """Privacy options entry point is not required."""

    REQUIRED = "required"
    """Privacy options entry point is required."""

    UNKNOWN = "unknown"
    """Privacy options requirement status is unknown."""


class DebugGeography(Enum):
    """
    Debug geography values used to test consent flows.

    Note:
        These only take effect on devices registered as test devices through
        :attr:`flet_ads.ConsentDebugSettings.test_identifiers`.
    """

    DISABLED = "disabled"
    """Debug geography disabled."""

    EEA = "eea"
    """Geography appears as in the EEA (European Economic Area) for debug devices."""

    REGULATED_US_STATE = "regulatedUsState"
    """Geography appears as in a regulated US State for debug devices."""

    OTHER = "other"
    """Geography appears as in a region with no regulation in force."""


@ft.value
class ConsentDebugSettings:
    """
    Debug settings to hardcode in consent requests, useful for testing the
    consent flow during development.
    """

    debug_geography: Optional[DebugGeography] = None
    """
    The geography to simulate when gathering consent on test devices.
    """

    test_identifiers: Optional[list[str]] = None
    """
    A list of device identifiers for which debug features are enabled.

    A device's hashed ID is printed to the device logs the first time a
    consent request is made from it.
    """


@ft.value
class ConsentRequestParameters:
    """
    Parameters sent when updating the user's consent information.
    """

    tag_for_under_age_of_consent: Optional[bool] = None
    """
    Whether the user is tagged as being under the age of consent.

    `False` means users are not under the age of consent.
    """

    consent_debug_settings: Optional[ConsentDebugSettings] = None
    """
    Debug settings to hardcode in test requests.
    """
