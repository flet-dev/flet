from typing import Optional, Union

import flet as ft
from flet_audio.types import (
    AudioContext,
    AudioDurationChangeEvent,
    AudioPositionChangeEvent,
    AudioStateChangeEvent,
    ReleaseMode,
)


@ft.control("Audio")
class Audio(ft.Service):
    """
    A control to simultaneously play multiple audio sources.

    Note:
        Keep a reference to an `Audio`, such as in a variable that your event handlers
        use, for as long as it should play. Flet removes services that no longer have
        live Python references after an event is handled, which stops their playback.
    """

    src: Optional[Union[str, bytes]] = None
    """
    The audio source.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.

    It can be left unset and assigned later, e.g. once the user picks a file.
    While it is unset, :meth:`flet_audio.Audio.play`,
    :meth:`flet_audio.Audio.resume` and :meth:`flet_audio.Audio.seek` raise an
    error.

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

    context: Optional[AudioContext] = None
    """
    Defines how this audio interacts with the device and with other audio on mobile
    platforms, such as whether it plays over other audio.

    If `None`, :attr:`flet_audio.AudioContext.respect_silence` is `False`, and
    :attr:`flet_audio.AudioContext.focus` depends on the platform:

    - On Android, `focus` is :attr:`flet_audio.AudioFocus.DUCK_OTHERS`, so every
      `Audio` of an app plays together, and other apps' audio usually gets quieter.
    - On iOS, `focus` is :attr:`flet_audio.AudioFocus.GAIN`, which interrupts other
      apps' audio.
    - On other platforms, this property is ignored.

    On iOS, a context applies to the whole app, so if another `Audio` of the app has
    applied one, all of it applies here instead of these values, `respect_silence`
    included. Setting this back to `None` after it was set applies these values.

    Should ideally be set when creating the control. On Android, changing it after a
    source is set prepares that source again, which restarts audio that is playing
    from the beginning. Changing it to :attr:`flet_audio.AudioFocus.GAIN` stops
    that audio instead, until :meth:`flet_audio.Audio.resume` is called.

    Note:
        If the app declares the `android.permission.MODIFY_AUDIO_SETTINGS` permission,
        setting this resets the device's audio mode to normal and turns its
        speakerphone off, which can interrupt a call that the app has in progress.
        The same reset happens once when the app starts, whether or not this is set.
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

    Note:
        - On Android and iOS, it doesn't fire when another app pauses this audio, nor
            on Android when a phone call rings, so the last reported state remains
            :attr:`flet_audio.AudioState.PLAYING`.
            :meth:`flet_audio.Audio.get_current_position` stops advancing meanwhile,
            and :meth:`flet_audio.Audio.resume` plays the audio again.
        - On iOS, audio with :attr:`flet_audio.ReleaseMode.LOOP` reports
            :attr:`flet_audio.AudioState.COMPLETED` each time it restarts, while it
            keeps playing.
    """

    on_position_change: Optional[ft.EventHandler[AudioPositionChangeEvent]] = None
    """
    Fires when audio position is changed.
    Will continuously update the position of the playback
    every 1 second if the status is playing.

    Can be used for a progress bar.

    Note:
        - On Android, it stops firing while something else pauses this audio, such as
            a ringing phone call or another app taking audio focus.
        - On iOS, it stops firing once audio with
            :attr:`flet_audio.ReleaseMode.LOOP` restarts for the first time.
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
                Defaults to the beginning of the audio.
        """
        await self._invoke_method(
            method_name="play",
            arguments={"position": position},
        )

    async def pause(self):
        """
        Pauses the audio that is currently playing.

        If you call :meth:`flet_audio.Audio.resume` later,
        the audio will resume from the point that it has been paused.

        A :meth:`flet_audio.Audio.play`, :meth:`flet_audio.Audio.resume` or
        :attr:`flet_audio.Audio.autoplay` still waiting for the audio to load is
        cancelled.
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
        you change the source or call :meth:`flet_audio.Audio.play`,
        :meth:`flet_audio.Audio.resume` or :meth:`flet_audio.Audio.seek`.

        Audio that is still loading is released once it has loaded. A
        :meth:`flet_audio.Audio.play`, :meth:`flet_audio.Audio.resume` or
        :attr:`flet_audio.Audio.autoplay` still waiting for the audio to load is
        cancelled.
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
