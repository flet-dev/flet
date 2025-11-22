from typing import Optional, Union

import flet as ft
from flet_audio.types import (
    AudioDurationChangeEvent,
    AudioPositionChangeEvent,
    AudioStateChangeEvent,
    ReleaseMode,
)


@ft.control("Audio")
class Audio(ft.Service):
    """
    A control to simultaneously play multiple audio sources.
    """

    src: Optional[Union[str, bytes]] = None
    """
    The audio source.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.

    Note:
        [Here](https://github.com/bluefireteam/audioplayers/blob/main/troubleshooting.md#supported-formats--encodings)
            is a list of supported audio formats.
    """

    autoplay: bool = False
    """
    Starts playing audio as soon as audio control is added to a page.

    Note:
        Autoplay works in desktop, mobile apps and Safari browser,
        but doesn't work in Chrome/Edge.
    """

    volume: ft.Number = 1.0
    """
    Sets the volume (amplitude).
    It's value ranges between `0.0` (mute) and `1.0` (maximum volume).
    Intermediate values are linearly interpolated.
    """

    balance: ft.Number = 0.0
    """
    Defines the stereo balance.

    * `-1` - The left channel is at full volume; the right channel is silent.
    * `1` - The right channel is at full volume; the left channel is silent.
    * `0` - Both channels are at the same volume.
    """

    playback_rate: ft.Number = 1.0
    """
    Defines the playback rate.

    Should ideally be set when creating the constructor.

    Note:
        - iOS and macOS have limits between `0.5x` and `2x`.
        - Android SDK version should be 23 or higher.
    """

    release_mode: ReleaseMode = ReleaseMode.RELEASE
    """
    Defines the release mode.
    """

    on_loaded: Optional[ft.ControlEventHandler["Audio"]] = None
    """
    Fires when an audio is loaded/buffered.
    """

    on_duration_change: Optional[ft.EventHandler[AudioDurationChangeEvent]] = None
    """
    Fires as soon as audio duration is available
    (it might take a while to download or buffer it).
    """

    on_state_change: Optional[ft.EventHandler[AudioStateChangeEvent]] = None
    """
    Fires when audio player state changes.
    """

    on_position_change: Optional[ft.EventHandler[AudioPositionChangeEvent]] = None
    """
    Fires when audio position is changed.
    Will continuously update the position of the playback
    every 1 second if the status is playing.

    Can be used for a progress bar.
    """

    on_seek_complete: Optional[ft.ControlEventHandler["Audio"]] = None
    """
    Fires on seek completions.
    An event is going to be sent as soon as the audio seek is finished.
    """

    async def play(self, position: ft.DurationValue = 0):
        """
        Starts playing audio from the specified `position`.

        Args:
            position: The position to start playback from.
        """
        await self._invoke_method(
            method_name="play",
            arguments={"position": position},
        )

    async def pause(self):
        """
        Pauses the audio that is currently playing.

        If you call [`resume()`][flet_audio.Audio.resume] later,
        the audio will resume from the point that it has been paused.
        """
        await self._invoke_method("pause")

    async def resume(self):
        """
        Resumes the audio that has been paused or stopped.
        """
        await self._invoke_method("resume")

    async def release(self):
        """
        Releases the resources associated with this media player.
        These are going to be fetched or buffered again as soon as
        you change the source or call [`resume()`][flet_audio.Audio.resume].
        """
        await self._invoke_method("release")

    async def seek(self, position: ft.DurationValue):
        """
        Moves the cursor to the desired position.

        Args:
            position: The position to seek/move to.
        """
        await self._invoke_method(
            method_name="seek",
            arguments={"position": position},
        )

    async def get_duration(self) -> Optional[ft.Duration]:
        """
        Get audio duration of the audio playback.

        It will be available as soon as the audio duration is available
        (it might take a while to download or buffer it if file is not local).

        Returns:
            The duration of audio playback.
        """
        return await self._invoke_method(
            method_name="get_duration",
        )

    async def get_current_position(self) -> Optional[ft.Duration]:
        """
        Get the current position of the audio playback.

        Returns:
            The current position of the audio playback.
        """
        return await self._invoke_method(
            method_name="get_current_position",
        )
