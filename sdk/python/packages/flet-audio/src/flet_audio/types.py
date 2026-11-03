from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    from flet_audio.audio import Audio  # noqa

__all__ = [
    "AudioContext",
    "AudioDurationChangeEvent",
    "AudioFocus",
    "AudioPositionChangeEvent",
    "AudioState",
    "AudioStateChangeEvent",
    "ReleaseMode",
]


class ReleaseMode(Enum):
    """
    Determines what happens to the player's resources (the buffered audio and
    the underlying native player) when playback finishes or is stopped, and
    therefore how quickly, and at what cost, the same audio can be played again.
    """

    RELEASE = "release"
    """
    Frees all resources once playback completes, as if
    :meth:`flet_audio.Audio.release` had been called automatically.
    This is the default mode.

    The buffered audio and the native player are released, so nothing is kept in
    memory while the audio is idle. Playing again is still supported, but the
    source is **loaded again from scratch** first (and a remote file is
    re-downloaded), which adds a short delay before playback starts.

    Best when replays are rare or may never happen and keeping memory usage to a
    minimum matters.

    Note:
        - On Android, the native media player is resource-intensive; this mode
            lets it go and re-buffers the data only when needed.
        - On iOS and macOS, behaves like :meth:`flet_audio.Audio.release`.
    """

    LOOP = "loop"
    """
    Automatically restarts playback from the beginning every time it completes,
    creating a continuous loop. All resources are kept buffered.

    Best for audio that should repeat indefinitely, such as background music.

    Note:
        Resources are never released automatically in this mode. To free them,
        change the source or call :meth:`flet_audio.Audio.release`.
    """

    STOP = "stop"
    """
    Stops playback when the audio completes but keeps all resources (the
    buffered audio and the native player) intact.

    Because nothing is released, playing again is **immediate**: the audio
    restarts straight from the retained buffer, with no reloading or
    re-downloading. The trade-off is that these resources stay in memory while
    the audio is idle.

    Best when you intend to replay the same audio and want instant,
    network-free playback (for example, short sound effects or repeated tones).
    """


class AudioState(Enum):
    """The state of the audio player."""

    STOPPED = "stopped"
    """The audio player is stopped."""

    PLAYING = "playing"
    """The audio player is currently playing audio."""

    PAUSED = "paused"
    """The audio player is paused and can be resumed."""

    COMPLETED = "completed"
    """The audio player has successfully reached the end of the audio."""

    DISPOSED = "disposed"
    """The audio player has been disposed of and should not be used anymore."""


@dataclass
class AudioStateChangeEvent(ft.Event["Audio"]):
    """
    Event triggered when the audio playback state changes.
    """

    state: AudioState
    """The current state of the audio player."""


@dataclass
class AudioPositionChangeEvent(ft.Event["Audio"]):
    """
    Event triggered when the audio playback position changes.
    """

    position: int
    """The current playback position in milliseconds."""


@dataclass
class AudioDurationChangeEvent(ft.Event["Audio"]):
    """
    Event triggered when the audio duration changes.
    """

    duration: ft.Duration
    """The duration of the audio."""


class AudioFocus(Enum):
    """
    How an :class:`~flet_audio.Audio` shares audio with other audio on mobile platforms.

    On Android, focus belongs to each player, so an :class:`~flet_audio.Audio` competes
    with others of the same app as it does with other apps. On iOS, it only decides how
    the app treats other apps, because all audio of an app always plays together.
    """

    GAIN = "gain"
    """
    Plays as the only audio.

    On Android, any other audio that is playing, including another
    :class:`~flet_audio.Audio` of the same app, is paused and doesn't resume on its
    own. On iOS, other apps' audio is interrupted.

    Best for music players.
    """

    DUCK_OTHERS = "duckOthers"
    """
    Lowers the volume of other apps' audio until this audio stops.

    On Android, another :class:`~flet_audio.Audio` of the same app keeps playing at
    its own volume.

    Warning:
        On iOS, can't be combined with :attr:`flet_audio.AudioContext.respect_silence`.
    """

    MIX_WITH_OTHERS = "mixWithOthers"
    """
    Plays over other audio, which isn't affected.

    On Android, nothing else pauses this audio, though Android still mutes it while a
    phone call is ringing, during which its position keeps advancing.

    Best for short sound effects that shouldn't lower the volume of other apps.

    Warning:
        On iOS, can't be combined with :attr:`flet_audio.AudioContext.respect_silence`.
    """


@ft.value(kw_only=True)
class AudioContext:
    """
    How an :class:`~flet_audio.Audio` interacts with the device and with other audio.

    Applies on Android and iOS. Other platforms ignore it.

    Note:
        On iOS, it applies to the whole app rather than to one
        :class:`~flet_audio.Audio`, so the one that applied it last decides for all
        others.
    """

    focus: Optional[AudioFocus] = None
    """
    How the audio shares with other audio.

    If `None`, :attr:`flet_audio.AudioFocus.DUCK_OTHERS` applies on Android, so
    every :class:`~flet_audio.Audio` of an app plays together, and
    :attr:`flet_audio.AudioFocus.GAIN` applies on iOS.
    """

    respect_silence: bool = False
    """
    Whether the audio follows the device's silent mode.

    On Android, this plays the audio as a ringtone, so it also follows the ringer
    volume instead of the media volume.

    Warning:
        On iOS, can't be combined with :attr:`focus` set to
        :attr:`flet_audio.AudioFocus.DUCK_OTHERS` or
        :attr:`flet_audio.AudioFocus.MIX_WITH_OTHERS`.
    """
