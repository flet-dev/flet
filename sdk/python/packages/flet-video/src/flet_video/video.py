"""
Video control definition for the flet-video package.
"""

from dataclasses import field
from typing import Optional

import flet as ft
from flet_video.types import (
    PlaylistMode,
    VideoConfiguration,
    VideoMedia,
    VideoSubtitleConfiguration,
    VideoSubtitleTrack,
)

__all__ = ["Video"]


@ft.control("Video")
class Video(ft.LayoutControl):
    """
    A control that displays a video from a playlist.
    """

    playlist: list[VideoMedia] = field(default_factory=list)
    """
    A list of `VideoMedia`s representing the video files to be played.
    """

    title: str = "flet-video"
    """
    Defines the name of the underlying window & process for native backend.
    This is visible inside the windows' volume mixer.
    """

    fit: ft.BoxFit = ft.BoxFit.CONTAIN
    """
    The box fit to use for the video.
    """

    fill_color: ft.ColorValue = ft.Colors.BLACK
    """
    Defines the color used to fill the video background.
    """

    wakelock: bool = True
    """
    Whether to acquire wake lock while playing the video.
    When `True`, device's display will not go to standby/sleep while
    the video is playing.
    """

    autoplay: bool = False
    """
    Whether the video should start playing automatically.
    """

    show_controls: bool = True
    """
    Whether to show the video player controls.
    """

    fullscreen: bool = False
    """
    Whether the video player is presented in fullscreen mode.

    Set to `True` to enter fullscreen or `False` to exit fullscreen programmatically.
    """

    muted: bool = False
    """
    Defines whether the video player should be started in muted state.
    """

    playlist_mode: Optional[PlaylistMode] = None
    """
    Represents the mode of playback for the playlist.
    """

    shuffle_playlist: bool = False
    """
    Defines whether the playlist should be shuffled.
    """

    volume: ft.Number = 100.0
    """
    Defines the volume of the video player.

    Note:
        It's value ranges between `0.0` to `100.0` (inclusive), where `0.0`
        is muted and `100.0` is the maximum volume.
        An exception will be raised if the value is outside this range.

    Raises:
        ValueError: If its value is not between `0.0` and `100.0` (inclusive).
    """

    playback_rate: ft.Number = 1.0
    """
    Defines the playback rate of the video player.
    """

    alignment: ft.Alignment = field(default_factory=lambda: ft.Alignment.CENTER)
    """
    Defines the Alignment of the viewport.
    """

    filter_quality: ft.FilterQuality = ft.FilterQuality.LOW
    """
    Filter quality of the texture used to render the video output.

    Note:
        Android was reported to show blurry images when using
        [`FilterQuality.HIGH`][flet.FilterQuality.HIGH].
        Prefer the usage of [`FilterQuality.MEDIUM`][flet.FilterQuality.MEDIUM]
        on this platform.
    """

    pause_upon_entering_background_mode: bool = True
    """
    Whether to pause the video when application enters background mode.
    """

    resume_upon_entering_foreground_mode: bool = False
    """
    Whether to resume the video when application enters foreground mode.
    Has effect only if [`pause_upon_entering_background_mode`][(c).] is also set to
    `True`.
    """

    pitch: ft.Number = 1.0
    """
    Defines the relative pitch of the video player.
    """

    configuration: VideoConfiguration = field(
        default_factory=lambda: VideoConfiguration()
    )
    """
    Additional configuration for the video player.
    """

    subtitle_configuration: VideoSubtitleConfiguration = field(
        default_factory=lambda: VideoSubtitleConfiguration()
    )
    """
    Defines the subtitle configuration for the video player.
    """

    subtitle_track: Optional[VideoSubtitleTrack] = None
    """
    Defines the subtitle track for the video player.
    """

    on_load: Optional[ft.ControlEventHandler["Video"]] = None
    """Fires when the video player is initialized and ready for playback."""

    on_enter_fullscreen: Optional[ft.ControlEventHandler["Video"]] = None
    """Fires when the video player enters fullscreen."""

    on_exit_fullscreen: Optional[ft.ControlEventHandler["Video"]] = None
    """Fires when the video player exits fullscreen"""

    on_error: Optional[ft.ControlEventHandler["Video"]] = None
    """
    Fires when an error occurs.

    Event handler argument's [`data`][flet.Event.data] property contains
    information about the error.
    """

    on_complete: Optional[ft.ControlEventHandler["Video"]] = None
    """Fires when a video player completes."""

    on_track_change: Optional[ft.ControlEventHandler["Video"]] = None
    """
    Fires when a video track changes.

    Event handler argument's [`data`][flet.Event.data] property contains
    the index of the new track.
    """

    def before_update(self):
        super().before_update()
        if not (0 <= self.volume <= 100):
            raise ValueError(
                f"volume must be between 0 and 100 inclusive, got {self.volume}"
            )

    async def play(self):
        """Starts playing the video."""
        await self._invoke_method("play")

    async def pause(self):
        """Pauses the video player."""
        await self._invoke_method("pause")

    async def play_or_pause(self):
        """
        Cycles between play and pause states of the video player,
        i.e., plays if paused and pauses if playing.
        """
        await self._invoke_method("play_or_pause")

    async def stop(self):
        """Stops the video player."""
        await self._invoke_method("stop")

    async def next(self):
        """Jumps to the next `VideoMedia` in the [`playlist`][(c).]."""
        await self._invoke_method("next")

    async def previous(self):
        """Jumps to the previous `VideoMedia` in the [`playlist`][(c).]."""
        await self._invoke_method("previous")

    async def seek(self, position: ft.DurationValue):
        """
        Seeks the currently playing `VideoMedia` from the
        [`playlist`][(c).] at the specified `position`.
        """
        await self._invoke_method(
            "seek",
            {"position": position},
        )

    async def jump_to(self, media_index: int):
        """
        Jumps to the `VideoMedia` at the specified `media_index`
        in the [`playlist`][(c).].
        """
        if not (-len(self.playlist) <= media_index < len(self.playlist)):
            raise IndexError("media_index is out of range")
        if media_index < 0:
            # dart doesn't support negative indexes
            media_index = len(self.playlist) + media_index
        await self._invoke_method(
            method_name="jump_to",
            arguments={"media_index": media_index},
        )

    async def playlist_add(self, media: VideoMedia):
        """Appends/Adds the provided `media` to the `playlist`."""
        if not media.resource:
            raise ValueError("media has no resource")
        await self._invoke_method(
            method_name="playlist_add",
            arguments={"media": media},
        )
        self.playlist.append(media)

    async def playlist_remove(self, media_index: int):
        """Removes the provided `media` from the `playlist`."""
        playlist_length = len(self.playlist)
        if not (-playlist_length <= media_index < playlist_length):
            raise IndexError("media_index is out of range")
        if media_index < 0:
            media_index = playlist_length + media_index
        await self._invoke_method(
            method_name="playlist_remove",
            arguments={"media_index": media_index},
        )
        self.playlist.pop(media_index)

    async def is_playing(self) -> bool:
        """
        Returns:
            `True` if the video player is currently playing, `False` otherwise.
        """
        return await self._invoke_method("is_playing")

    async def is_completed(self) -> bool:
        """
        Returns:
            `True` if video player has reached the end of
                the currently playing media, `False` otherwise.
        """
        return await self._invoke_method("is_completed")

    async def get_duration(self) -> ft.Duration:
        """
        Returns:
            The duration of the currently playing media.
        """
        return await self._invoke_method("get_duration")

    async def get_current_position(self) -> ft.Duration:
        """
        Returns:
            The current position of the currently playing media.
        """
        return await self._invoke_method("get_current_position")
