"""
Type definitions and configuration objects for flet-video.
"""

from dataclasses import field
from enum import Enum
from typing import Optional, Union

import flet as ft

__all__ = [
    "AdaptiveVideoControls",
    "MaterialDesktopVideoControls",
    "MaterialVideoControls",
    "PlaylistMode",
    "VideoBarItem",
    "VideoConfiguration",
    "VideoControls",
    "VideoControlsMode",
    "VideoFullscreenButton",
    "VideoMedia",
    "VideoPlayOrPauseButton",
    "VideoPositionIndicator",
    "VideoSkipNextButton",
    "VideoSkipPreviousButton",
    "VideoSpacer",
    "VideoSubtitleConfiguration",
    "VideoSubtitleTrack",
    "VideoVolumeButton",
]


class PlaylistMode(Enum):
    """Defines the playback mode for the video playlist."""

    NONE = "none"
    """End playback once end of the playlist is reached."""

    SINGLE = "single"
    """Indefinitely loop over the currently playing file in the playlist."""

    LOOP = "loop"
    """Loop over the playlist & restart it from beginning once end is reached."""


class VideoControlsMode(Enum):
    """Modes that can receive different :attr:`Video.controls` values."""

    NORMAL = "normal"
    """Controls used when the video is not fullscreen."""

    FULLSCREEN = "fullscreen"
    """Controls used when the video is fullscreen."""

    DEFAULT = "default"
    """Fallback controls used when no applicable mode-specific value is provided."""


@ft.value
class VideoMedia:
    """Represents a media resource for video playback."""

    resource: str
    """URI of the media resource."""

    http_headers: Optional[dict[str, str]] = None
    """HTTP headers to be used for the media resource."""

    extras: Optional[dict[str, str]] = None
    """Additional metadata for the media resource."""


@ft.value
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
    Specifying this option will cause :attr:`width` & :attr:`height` to be ignored.
    """

    mpv_properties: Optional[dict[str, Union[str, int, float, bool]]] = None
    """
    Extra mpv/libmpv properties to set on
    native backends (Windows/macOS/Linux/iOS/Android).

    The keys are mpv option/property names without the leading `--`. Values can be
    `str`, `int`, `float` or `bool`. All values are converted to strings before being
    passed to mpv; boolean values are converted to `"yes"` / `"no"`.

    Full list of mpv options: https://mpv.io/manual/stable/#options

    Example:
        ```python
        >>> VideoConfiguration(
                mpv_properties={
                    "profile": "low-latency",   # --profile=low-latency
                    "untimed": True,            # --untimed
                    "volume": 80,               # --volume=80
                }
            )
        ```
    """


@ft.value
class VideoBarItem:
    """Base class for built-in video controls button bar items."""

    _type: str = field(default="", init=False, repr=False)
    """
    Identifies which built-in video controls button bar item should be used.

    This value is fixed by each concrete item class.
    """


@ft.value
class VideoPlayOrPauseButton(VideoBarItem):
    """A built-in play/pause button item."""

    _type: str = field(default="playOrPauseButton", init=False, repr=False)
    """
    Identifies this item as a built-in play/pause button.
    """

    icon_size: Optional[ft.Number] = None
    """
    Overrides the icon size.
    """

    icon_color: Optional[ft.ColorValue] = None
    """
    Overrides the icon color.
    """


@ft.value
class VideoSkipNextButton(VideoBarItem):
    """A built-in skip next button item."""

    _type: str = field(default="skipNextButton", init=False, repr=False)
    """
    Identifies this item as a built-in skip next button.
    """

    icon: Optional[ft.Control] = None
    """
    Icon displayed by the button.

    If omitted, the default skip next icon is used.
    """

    icon_size: Optional[ft.Number] = None
    """
    Overrides the icon size.
    """

    icon_color: Optional[ft.ColorValue] = None
    """
    Overrides the icon color.
    """


@ft.value
class VideoSkipPreviousButton(VideoBarItem):
    """A built-in skip previous button item."""

    _type: str = field(default="skipPreviousButton", init=False, repr=False)
    """
    Identifies this item as a built-in skip previous button.
    """

    icon: Optional[ft.Control] = None
    """
    Icon displayed by the button.

    If omitted, the default skip previous icon is used.
    """

    icon_size: Optional[ft.Number] = None
    """
    Overrides the icon size.
    """

    icon_color: Optional[ft.ColorValue] = None
    """
    Overrides the icon color.
    """


@ft.value
class VideoFullscreenButton(VideoBarItem):
    """A built-in fullscreen button item."""

    _type: str = field(default="fullscreenButton", init=False, repr=False)
    """
    Identifies this item as a built-in fullscreen button.
    """

    icon: Optional[ft.Control] = None
    """
    Icon displayed by the button.

    If omitted, the default fullscreen icon is used.
    """

    icon_size: Optional[ft.Number] = None
    """
    Overrides the icon size.
    """

    icon_color: Optional[ft.ColorValue] = None
    """
    Overrides the icon color.
    """


@ft.value
class VideoPositionIndicator(VideoBarItem):
    """A built-in playback position indicator item."""

    _type: str = field(default="positionIndicator", init=False, repr=False)
    """
    Identifies this item as a built-in playback position indicator.
    """

    text_style: Optional[ft.TextStyle] = None
    """
    Overrides the text style.
    """


@ft.value
class VideoSpacer(VideoBarItem):
    """A built-in spacer item for video controls button bars."""

    _type: str = field(default="spacer", init=False, repr=False)
    """
    Identifies this item as a built-in spacer.
    """

    flex: int = 1
    """
    The flex factor to use for the spacer.
    """


@ft.value
class VideoVolumeButton(VideoBarItem):
    """
    A built-in volume button and slider item.

    Note:
        This item is currently rendered only by :class:`MaterialDesktopVideoControls`.
    """

    _type: str = field(default="volumeButton", init=False, repr=False)
    """
    Identifies this item as a built-in Material desktop volume button.
    """

    icon_size: Optional[ft.Number] = None
    """
    Overrides the icon size.
    """

    icon_color: Optional[ft.ColorValue] = None
    """
    Overrides the icon color.
    """

    volume_mute_icon: Optional[ft.Control] = None
    """
    Icon displayed when volume is muted.

    If omitted, the default muted volume icon is used.
    """

    volume_low_icon: Optional[ft.Control] = None
    """
    Icon displayed when volume is low.

    If omitted, the default low volume icon is used.
    """

    volume_high_icon: Optional[ft.Control] = None
    """
    Icon displayed when volume is high.

    If omitted, the default high volume icon is used.
    """

    slider_width: Optional[ft.Number] = None
    """
    Width of the volume slider.
    """


@ft.value
class VideoControls:
    """Base class for built-in video controls."""

    _type: str = field(default="", init=False, repr=False)
    """
    Identifies which built-in controls implementation should be used.

    This value is fixed by each concrete controls class.
    """


@ft.value
class MaterialVideoControls(VideoControls):
    """Touch-oriented Material video controls."""

    _type: str = field(default="material", init=False, repr=False)
    """
    Identifies this value as Material video controls.
    """

    # Behavior

    display_seek_bar: bool = True
    """
    Whether to display seek bar.
    """

    automatically_imply_skip_next_button: bool = True
    """
    Whether a skip next button should be displayed if there are more than one
    videos in the playlist.
    """

    automatically_imply_skip_previous_button: bool = True
    """
    Whether a skip previous button should be displayed if there are more than one
    videos in the playlist.
    """

    volume_gesture: bool = False
    """
    Whether to modify volume on vertical drag gesture on the right side of the screen.
    """

    brightness_gesture: bool = False
    """
    Whether to modify screen brightness on vertical drag gesture on the left side
    of the screen.
    """

    seek_gesture: bool = False
    """
    Whether to seek on horizontal drag gesture.
    """

    gestures_enabled_while_controls_visible: bool = True
    """
    Whether to allow gesture controls to work while controls are visible.

    Note:
        This option is ignored when gestures are disabled.
    """

    seek_on_double_tap: bool = False
    """
    Whether to enable double tap to seek on left or right side of the screen.
    """

    seek_on_double_tap_enabled_while_controls_visible: bool = True
    """
    Whether to allow double tap to seek on left or right side of the screen to
    work while controls are visible.

    Note:
        This option is ignored when :attr:`seek_on_double_tap` is `False`.
    """

    seek_on_double_tap_layout_taps_ratios: list[int] = field(
        default_factory=lambda: [1, 1, 1]
    )
    """
    Width proportions for the backward seek, instant tap, and forward seek areas
    when a double tap occurs on the video widget.
    """

    seek_on_double_tap_layout_widget_ratios: list[int] = field(
        default_factory=lambda: [1, 1, 1]
    )
    """
    Width proportions for the visual indicators shown during backward seek,
    instant tap, and forward seek actions.
    """

    seek_on_double_tap_backward_duration: ft.DurationValue = 10000
    """
    Duration of seek on double tap backward.
    """

    seek_on_double_tap_forward_duration: ft.DurationValue = 10000
    """
    Duration of seek on double tap forward.
    """

    visible_on_mount: bool = False
    """
    Whether the controls are initially visible.
    """

    speed_up_on_long_press: bool = False
    """
    Whether to speed up on long press.
    """

    speed_up_factor: ft.Number = 2.0
    """
    Factor to speed up on long press.
    """

    vertical_gesture_sensitivity: ft.Number = 100
    """
    Gesture sensitivity on vertical drag gestures, the higher the value is the
    less sensitive the gesture.
    """

    horizontal_gesture_sensitivity: ft.Number = 1000
    """
    Gesture sensitivity on horizontal drag gestures, the higher the value is the
    less sensitive the gesture.
    """

    backdrop_color: Optional[ft.ColorValue] = "#66000000"
    """
    Color of backdrop that comes up when controls are visible.
    """

    # Generic

    padding: Optional[ft.PaddingValue] = None
    """
    Padding around the controls.
    """

    controls_hover_duration: ft.DurationValue = 3000
    """
    Duration after which the controls will be hidden when there is no mouse movement.
    """

    controls_transition_duration: ft.DurationValue = 300
    """
    Duration for which the controls will be animated when shown or hidden.
    """

    initial_volume: ft.Number = 0.5
    """
    Initial volume value used by the volume gesture indicator.

    It ranges from `0.0` to `1.0`.
    """

    initial_brightness: ft.Number = 0.5
    """
    Initial brightness value used by the brightness gesture indicator.

    It ranges from `0.0` to `1.0`.
    """

    # Button bar

    primary_button_bar: Optional[list[Union[ft.Control, VideoBarItem]]] = None
    """
    Controls displayed in the primary button bar.

    Set to a list to replace the primary button bar, or an empty list to hide
    it; if `None`, the native default is:
    ```python
    [
        ftv.VideoSpacer(flex=2),
        ftv.VideoSkipPreviousButton(),
        ftv.VideoSpacer(),
        ftv.VideoPlayOrPauseButton(icon_size=48.0),
        ftv.VideoSpacer(),
        ftv.VideoSkipNextButton(),
        ftv.VideoSpacer(flex=2),
    ]
    ```
    """

    top_button_bar: Optional[list[Union[ft.Control, VideoBarItem]]] = None
    """
    Controls displayed in the top button bar.

    Set to a list to replace the top button bar, or an empty list to hide it;
    if `None`, the native default is an empty list.
    """

    top_button_bar_margin: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.symmetric(horizontal=16.0)
    )
    """
    Margin around the top button bar.
    """

    bottom_button_bar: Optional[list[Union[ft.Control, VideoBarItem]]] = None
    """
    Controls displayed in the bottom button bar.

    Set to a list to replace the bottom button bar, or an empty list to hide
    it; if `None`, the native default is:
    ```python
    [
        ftv.VideoPositionIndicator(),
        ftv.VideoSpacer(),
        ftv.VideoFullscreenButton(),
    ]
    ```
    """

    bottom_button_bar_margin: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.only(left=16.0, right=8.0)
    )
    """
    Margin around the button bar.
    """

    button_bar_height: ft.Number = 56.0
    """
    Height of the button bar.
    """

    button_bar_button_size: ft.Number = 24.0
    """
    Size of the button bar buttons.
    """

    button_bar_button_color: ft.ColorValue = "#FFFFFFFF"
    """
    Color of the button bar buttons.
    """

    # Seek bar

    seek_bar_margin: ft.PaddingValue = 0
    """
    Margin around the seek bar.
    """

    seek_bar_height: ft.Number = 2.4
    """
    Height of the seek bar.
    """

    seek_bar_container_height: ft.Number = 36.0
    """
    Height of the seek bar container.
    """

    seek_bar_color: ft.ColorValue = "#3DFFFFFF"
    """
    Color of the seek bar.
    """

    seek_bar_position_color: ft.ColorValue = "#FFFF0000"
    """
    Color of the playback position section in the seek bar.
    """

    seek_bar_buffer_color: ft.ColorValue = "#3DFFFFFF"
    """
    Color of the playback buffer section in the seek bar.
    """

    seek_bar_thumb_size: ft.Number = 12.8
    """
    Size of the seek bar thumb.
    """

    seek_bar_thumb_color: ft.ColorValue = "#FFFF0000"
    """
    Color of the seek bar thumb.
    """

    seek_bar_alignment: ft.Alignment = field(
        default_factory=lambda: ft.Alignment.BOTTOM_CENTER
    )
    """
    Alignment of seek bar inside the seek bar container.
    """

    # Subtitle

    shift_subtitles_on_controls_visibility_change: bool = False
    """
    Whether to shift the subtitles upwards when the controls are visible.
    """


@ft.value
class MaterialDesktopVideoControls(VideoControls):
    """Desktop-oriented Material video controls."""

    _type: str = field(default="materialDesktop", init=False, repr=False)
    """
    Identifies this value as Material desktop video controls.
    """

    # Behavior

    display_seek_bar: bool = True
    """
    Whether to display seek bar.
    """

    automatically_imply_skip_next_button: bool = True
    """
    Whether a skip next button should be displayed if there are more than one
    videos in the playlist.
    """

    automatically_imply_skip_previous_button: bool = True
    """
    Whether a skip previous button should be displayed if there are more than one
    videos in the playlist.
    """

    modify_volume_on_scroll: bool = True
    """
    Modify volume on mouse scroll.
    """

    toggle_fullscreen_on_double_press: bool = True
    """
    Whether to toggle fullscreen on double press.
    """

    hide_mouse_on_controls_removal: bool = False
    """
    Whether to hide mouse on controls removal.

    Note:
        On most platforms, the mouse must move before it becomes hidden. It
        works on macOS without moving the mouse.
    """

    play_and_pause_on_tap: bool = False
    """
    Whether to toggle play and pause on tap.
    """

    visible_on_mount: bool = False
    """
    Whether the controls are initially visible.
    """

    # Generic

    padding: Optional[ft.PaddingValue] = None
    """
    Padding around the controls.
    """

    controls_hover_duration: ft.DurationValue = 3000
    """
    Duration after which the controls will be hidden when there is no mouse movement.
    """

    controls_transition_duration: ft.DurationValue = 150
    """
    Duration for which the controls will be animated when shown or hidden.
    """

    # Button bar

    primary_button_bar: Optional[list[Union[ft.Control, VideoBarItem]]] = None
    """
    Controls displayed in the primary button bar.

    Set to a list to replace the primary button bar, or an empty list to hide
    it; if `None`, the native default is an empty list.
    """

    top_button_bar: Optional[list[Union[ft.Control, VideoBarItem]]] = None
    """
    Controls displayed in the top button bar.

    Set to a list to replace the top button bar, or an empty list to hide it;
    if `None`, the native default is an empty list.
    """

    top_button_bar_margin: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.symmetric(horizontal=16.0)
    )
    """
    Margin around the top button bar.
    """

    bottom_button_bar: Optional[list[Union[ft.Control, VideoBarItem]]] = None
    """
    Controls displayed in the bottom button bar.

    Set to a list to replace the bottom button bar, or an empty list to hide
    it; if `None`, the native default is:
    ```python
    [
        ftv.VideoSkipPreviousButton(),
        ftv.VideoPlayOrPauseButton(),
        ftv.VideoSkipNextButton(),
        ftv.VideoSpacer(),
        ftv.VideoPositionIndicator(),
        ftv.VideoFullscreenButton(),
        ftv.VideoVolumeButton(),
    ]
    ```
    """

    bottom_button_bar_margin: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.symmetric(horizontal=16.0)
    )
    """
    Margin around the bottom button bar.
    """

    button_bar_height: ft.Number = 56.0
    """
    Height of the button bar.
    """

    button_bar_button_size: ft.Number = 28.0
    """
    Size of the button bar buttons.
    """

    button_bar_button_color: ft.ColorValue = "#FFFFFFFF"
    """
    Color of the button bar buttons.
    """

    # Seek bar

    seek_bar_transition_duration: ft.DurationValue = 300
    """
    Duration for which the seek bar will be animated when the user seeks.
    """

    seek_bar_thumb_transition_duration: ft.DurationValue = 150
    """
    Duration for which the seek bar thumb will be animated when the user seeks.
    """

    seek_bar_margin: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.symmetric(horizontal=16.0)
    )
    """
    Margin around the seek bar.
    """

    seek_bar_height: ft.Number = 3.2
    """
    Height of the seek bar.
    """

    seek_bar_hover_height: ft.Number = 5.6
    """
    Height of the seek bar when hovered.
    """

    seek_bar_container_height: ft.Number = 36.0
    """
    Height of the seek bar container.
    """

    seek_bar_color: ft.ColorValue = "#3DFFFFFF"
    """
    Color of the seek bar.
    """

    seek_bar_hover_color: ft.ColorValue = "#3DFFFFFF"
    """
    Color of the hovered section in the seek bar.
    """

    seek_bar_position_color: ft.ColorValue = "#FFFF0000"
    """
    Color of the playback position section in the seek bar.
    """

    seek_bar_buffer_color: ft.ColorValue = "#3DFFFFFF"
    """
    Color of the playback buffer section in the seek bar.
    """

    seek_bar_thumb_size: ft.Number = 12.0
    """
    Size of the seek bar thumb.
    """

    seek_bar_thumb_color: ft.ColorValue = "#FFFF0000"
    """
    Color of the seek bar thumb.
    """

    # Volume bar

    volume_bar_color: ft.ColorValue = "#3DFFFFFF"
    """
    Color of the volume bar.
    """

    volume_bar_active_color: ft.ColorValue = "#FFFFFFFF"
    """
    Color of the active region in the volume bar.
    """

    volume_bar_thumb_size: ft.Number = 12.0
    """
    Size of the volume bar thumb.
    """

    volume_bar_thumb_color: ft.ColorValue = "#FFFFFFFF"
    """
    Color of the volume bar thumb.
    """

    volume_bar_transition_duration: ft.DurationValue = 150
    """
    Duration for which the volume bar will be animated when the user hovers.
    """

    # Subtitle

    shift_subtitles_on_controls_visibility_change: bool = True
    """
    Whether to shift the subtitles upwards when the controls are visible.
    """


@ft.value
class AdaptiveVideoControls(VideoControls):
    """
    Platform-adaptive video controls.

    Adaptive controls select the controls implementation at runtime based on the
    current :attr:`flet.Page.platform`:
    - Android and iOS use Material controls.
    - macOS, Windows, and Linux use Material desktop controls.
    - Other platforms show no built-in controls.

    Use :attr:`material` and :attr:`material_desktop` to configure the controls
    family that may be selected for each platform.
    """

    _type: str = field(default="adaptive", init=False, repr=False)
    """
    Identifies this value as adaptive video controls.
    """

    material: Optional[MaterialVideoControls] = None
    """
    Controls used when adaptive controls select Material controls.

    If omitted, Material controls use the default
    :class:`MaterialVideoControls` value.
    """

    material_desktop: Optional[MaterialDesktopVideoControls] = None
    """
    Controls used when adaptive controls select Material desktop controls.

    If omitted, Material desktop controls use the default
    :class:`MaterialDesktopVideoControls` value.
    """


@ft.value
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


@ft.value
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
