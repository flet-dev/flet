"""
Type definitions and configuration objects for flet-video.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import flet as ft

__all__ = [
    "PlaylistMode",
    "VideoConfiguration",
    "VideoMedia",
    "VideoSubtitleConfiguration",
    "VideoSubtitleTrack",
]


class PlaylistMode(Enum):
    """Defines the playback mode for the video playlist."""

    NONE = "none"
    """End playback once end of the playlist is reached."""

    SINGLE = "single"
    """Indefinitely loop over the currently playing file in the playlist."""

    LOOP = "loop"
    """Loop over the playlist & restart it from beginning once end is reached."""


@dataclass
class VideoMedia:
    """Represents a media resource for video playback."""

    resource: str
    """URI of the media resource."""

    http_headers: Optional[dict[str, str]] = None
    """HTTP headers to be used for the media resource."""

    extras: Optional[dict[str, str]] = None
    """Additional metadata for the media resource."""


@dataclass
class VideoConfiguration:
    """Additional configuration for video playback."""

    output_driver: Optional[str] = None
    """
    Sets the [--vo](https://mpv.io/manual/stable/#options-vo) property
    on native backend.

    The default value is platform dependent:
        - Windows, GNU/Linux, macOS & iOS : `"libmpv"`
        - Android: `"gpu"`
    """

    hardware_decoding_api: Optional[str] = None
    """
    Sets the [--hwdec](https://mpv.io/manual/stable/#options-hwdec)
    property on native backend.

    The default value is platform dependent:
        - Windows, GNU/Linux, macOS & iOS : `"auto"`
        - Android: `"auto-safe"`
    """

    enable_hardware_acceleration: bool = True
    """
    Whether to enable hardware acceleration.
    When disabled, may cause battery drain, device heating, and high CPU usage.
    """

    width: Optional[ft.Number] = None
    """
    The fixed width for the video output.
    """

    height: Optional[ft.Number] = None
    """
    The fixed height for the video output.
    """

    scale: ft.Number = 1.0
    """
    The scale for the video output.
    Specifying this option will cause [`width`][(c).] & [`height`][(c).] to be ignored.
    """


@dataclass
class VideoSubtitleTrack:
    """Represents a subtitle track for a video."""

    src: str
    """
    The subtitle source.

    Supported values:
        - A URL (e.g. "https://example.com/subs.srt" or "www.example.com/sub.vtt")
        - An absolute local file path (not supported on the web platform)
        - A raw subtitle text string (e.g. the full contents of an SRT/VTT file)
    """

    title: Optional[str] = None
    """The title of the subtitle track, e.g. 'English'."""

    language: Optional[str] = None
    """The language of the subtitle track, e.g. 'en'."""

    channels_count: Optional[int] = None
    """
    The number of audio channels detected in the media.
    """

    channels: Optional[str] = None
    """
    Channel layout string describing the spatial arrangement of channels.
    """

    sample_rate: Optional[int] = None
    """
    Audio sampling rate in hertz.
    """

    fps: Optional[ft.Number] = None
    """
    Video frames per second.
    """

    bitrate: Optional[int] = None
    """
    Overall media bitrate in bits per second.
    """

    rotate: Optional[int] = None
    """
    Rotation metadata in degrees to apply when rendering the video.
    """

    par: Optional[ft.Number] = None
    """
    Pixel aspect ratio value.
    """

    audio_channels: Optional[int] = None
    """
    Explicit audio channel count override.
    """

    album_art: Optional[bool] = None
    """
    Whether the track represents album art rather than timed media.
    """

    codec: Optional[str] = None
    """
    Codec identifier for the media stream.
    """

    decoder: Optional[str] = None
    """
    Decoder name used to process the media stream.
    """

    @classmethod
    def none(cls) -> "VideoSubtitleTrack":
        """No subtitle track. Disables subtitle output."""
        return VideoSubtitleTrack(src="none")

    @classmethod
    def auto(cls) -> "VideoSubtitleTrack":
        """Default subtitle track. Selects the first subtitle track."""
        return VideoSubtitleTrack(src="auto")


@dataclass
class VideoSubtitleConfiguration:
    """Represents the configuration for video subtitles."""

    text_style: ft.TextStyle = field(
        default_factory=lambda: ft.TextStyle(
            height=1.4,
            size=32.0,
            letter_spacing=0.0,
            word_spacing=0.0,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.NORMAL,
            bgcolor=ft.Colors.BLACK_54,
        )
    )
    """The text style to be used for the subtitles."""

    text_scale_factor: ft.Number = 1.0
    """
    Defines the scale factor for the subtitle text.
    """

    text_align: ft.TextAlign = ft.TextAlign.CENTER
    """
    The text alignment to be used for the subtitles.
    """

    padding: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding(left=16.0, top=0.0, right=16.0, bottom=24.0)
    )
    """
    The padding to be used for the subtitles.
    """

    visible: bool = True
    """
    Whether the subtitles should be visible or not.
    """
