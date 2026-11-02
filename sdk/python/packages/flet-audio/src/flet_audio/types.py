from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    from flet_audio.audio import Audio  # noqa

__all__ = [
    "AudioContext",
    "AudioContextFocus",
    "AudioContextRoute",
    "AudioDurationChangeEvent",
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


class AudioContextFocus(Enum):
    """
    How the audio player requests and handles audio focus on mobile platforms.
    """

    GAIN = "gain"
    """
    Requests permanent audio focus, pausing other background audio apps.
    """

    DUCK_OTHERS = "duckOthers"
    """
    Lowers the volume of other audio apps while this audio plays.

    Warning:
        Due to iOS platform limitations, cannot be combined with
        :attr:`~flet_audio.AudioContext.respect_silence` set to `True`.
    """

    MIX_WITH_OTHERS = "mixWithOthers"
    """
    Mixes with other background audio apps without pausing or ducking them.

    Warning:
        Due to iOS platform limitations, cannot be combined with
        :attr:`~flet_audio.AudioContext.respect_silence` set to `True`.
    """


class AudioContextRoute(Enum):
    """
    Audio output routing behavior.
    """

    SYSTEM = "system"
    """Uses the default system audio route."""

    SPEAKER = "speaker"
    """
    Forces audio output through the built-in speaker.

    Warning:
        Due to iOS platform limitations, cannot be combined with
        :attr:`~flet_audio.AudioContext.respect_silence` set to `True`.
    """

    EARPIECE = "earpiece"
    """Routes audio output to the earpiece receiver."""


@ft.value(kw_only=True)
class AudioContext:
    """
    Cross-platform configuration for native audio session and focus behavior.

    Unset fields (`None`) are filled in when the context is applied on mobile:
    route as :attr:`~flet_audio.AudioContextRoute.SYSTEM`, focus as
    :attr:`~flet_audio.AudioContextFocus.GAIN`, and `respect_silence` /
    `stay_awake` as `False`.

    Note:
        On iOS, audio context cannot be handled for each player individually,
        so setting this property on an :class:`~flet_audio.Audio` instance
        applies the context globally for the app.

        Meaningful mainly on Android and iOS; desktop and web ignore it.
    """

    route: Optional[AudioContextRoute] = None
    """
    The audio output route (:attr:`~flet_audio.AudioContextRoute.SYSTEM`,
    :attr:`~flet_audio.AudioContextRoute.SPEAKER`, or
    :attr:`~flet_audio.AudioContextRoute.EARPIECE`).

    If unset (`None`), mobile platforms behave as
    :attr:`~flet_audio.AudioContextRoute.SYSTEM`.
    """

    focus: Optional[AudioContextFocus] = None
    """
    The audio focus mode (:attr:`~flet_audio.AudioContextFocus.GAIN`,
    :attr:`~flet_audio.AudioContextFocus.DUCK_OTHERS`, or
    :attr:`~flet_audio.AudioContextFocus.MIX_WITH_OTHERS`).

    If unset (`None`), mobile platforms behave as
    :attr:`~flet_audio.AudioContextFocus.GAIN`.
    """

    respect_silence: Optional[bool] = None
    """
    Whether the audio should be muted when the device is in silent/ringer mode.

    If unset (`None`), mobile platforms behave as `False`
    (audio can play while the device is silenced).

    Warning:
        Due to iOS platform limitations, setting this to `True` cannot be
        combined with :attr:`~flet_audio.AudioContextFocus.DUCK_OTHERS`,
        :attr:`~flet_audio.AudioContextFocus.MIX_WITH_OTHERS`, or
        :attr:`~flet_audio.AudioContextRoute.SPEAKER`.
    """

    stay_awake: Optional[bool] = None
    """
    Whether to keep the device awake (acquire a wake lock) while playing audio.

    If unset (`None`), mobile platforms behave as `False`.
    """
