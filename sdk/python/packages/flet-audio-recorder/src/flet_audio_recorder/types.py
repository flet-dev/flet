from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Optional

import flet as ft

if TYPE_CHECKING:
    from .audio_recorder import AudioRecorder  # noqa

__all__ = [
    "AndroidAudioSource",
    "AndroidRecorderConfiguration",
    "AudioEncoder",
    "AudioRecorderConfiguration",
    "AudioRecorderState",
    "AudioRecorderStateChangeEvent",
    "InputDevice",
    "IosAudioCategoryOption",
    "IosRecorderConfiguration",
]


class AudioRecorderState(Enum):
    """State of the audio recorder."""

    STOPPED = "stopped"
    """The audio recorder is stopped and not recording."""

    RECORDING = "recording"
    """The audio recorder is currently recording audio."""

    PAUSED = "paused"
    """The audio recorder is paused and can be resumed."""


@dataclass
class AudioRecorderStateChangeEvent(ft.Event["AudioRecorder"]):
    state: AudioRecorderState
    """The new state of the audio recorder."""


class AudioEncoder(Enum):
    """
    Represents the different audio encoders for audio recording.
    """

    AACLC = "aacLc"
    """
    Advanced Audio Codec Low Complexity.
    A commonly used encoder for streaming and general audio recording.
    """

    AACELD = "aacEld"
    """
    Advanced Audio Codec Enhanced Low Delay.
    Suitable for low-latency applications like VoIP.
    """

    AACHE = "aacHe"
    """
    Advanced Audio Codec High Efficiency.
    Optimized for high-quality audio at lower bit rates.
    """

    AMRNB = "amrNb"
    """
    Adaptive Multi-Rate Narrow Band.
    Used for speech audio in mobile communication.
    """

    AMRWB = "amrWb"
    """
    Adaptive Multi-Rate Wide Band.
    Used for higher-quality speech audio.
    """

    OPUS = "opus"
    """
    A codec designed for both speech and audio applications,
    known for its versatility.
    """

    FLAC = "flac"
    """
    Free Lossless Audio Codec.
    Provides high-quality lossless audio compression.
    """

    WAV = "wav"
    """
    Standard audio format used for raw, uncompressed audio data.
    """

    PCM16BITS = "pcm16bits"
    """
    Pulse Code Modulation with 16-bit depth, used for high-fidelity audio.
    """


class AndroidAudioSource(Enum):
    """Android-specific audio source types."""

    DEFAULT_SOURCE = "defaultSource"
    """Default audio source."""

    MIC = "mic"
    """Microphone audio source."""

    VOICE_UPLINK = "voiceUplink"
    """Voice call uplink (Tx) audio source."""

    VOICE_DOWNLINK = "voiceDownlink"
    """Voice call downlink (Rx) audio source."""

    VOICE_CALL = "voiceCall"
    """Voice call uplink + downlink audio source."""

    CAMCORDER = "camcorder"
    """
    Microphone audio source tuned for video recording,
    with the same orientation as the camera, if available.
    """

    VOICE_RECOGNITION = "voiceRecognition"
    """Microphone audio source tuned for voice recognition."""

    VOICE_COMMUNICATION = "voiceCommunication"
    """Microphone audio source tuned for voice communications such as VoIP."""

    REMOTE_SUBMIX = "remoteSubMix"
    """Audio source for a submix of audio streams to be presented remotely."""

    UNPROCESSED = "unprocessed"
    """
    Microphone audio source tuned for unprocessed (raw) sound if available,
    behaves like `DEFAULT_SOURCE` otherwise.
    """

    VOICE_PERFORMANCE = "voicePerformance"
    """
    Source for capturing audio meant to be processed in real time
    and played back for live performance (e.g karaoke).
    """


@dataclass
class AndroidRecorderConfiguration:
    """Android specific configuration for recording."""

    use_legacy: bool = False
    """
    Whether to use the Android MediaRecorder.

    While advanced recorder (the default) unlocks additionnal features,
    the legacy recorder is stability oriented.
    """

    mute_audio: bool = False
    """
    Whether to mute all audio streams like alarms, music, ring, etc.

    This is useful when you want to record audio without any background noise.
    The streams are restored to their previous state after recording is stopped
    and will stay at current state on pause/resume.
    """

    manage_bluetooth: bool = True
    """
    Try to start a bluetooth audio connection to a headset (Bluetooth SCO).
    """

    audio_source: AndroidAudioSource = AndroidAudioSource.DEFAULT_SOURCE
    """
    Defines the audio source.

    An audio source defines both a default physical source of audio signal,
    and a recording configuration.
    Some effects are available or not depending on this source.

    Most of the time, you should use
    [`AndroidAudioSource.DEFAULT_SOURCE`][(p).] or
    [`AndroidAudioSource.MIC`][(p).].
    """


class IosAudioCategoryOption(Enum):
    """
    Audio behaviors.

    Each option is valid only for specific audio session categories.
    """

    MIX_WITH_OTHERS = "mixWithOthers"
    """
    Whether audio from this session mixes with audio
    from active sessions in other audio apps.
    """

    DUCK_OTHERS = "duckOthers"
    """
    Reduces the volume of other audio sessions while audio from this session plays.
    """

    ALLOW_BLUETOOTH = "allowBluetooth"
    """
    Bluetooth hands-free devices appear as available input routes.
    """

    DEFAULT_TO_SPEAKER = "defaultToSpeaker"
    """
    Audio from the session defaults to the built-in speaker instead of the receiver.
    """

    INTERRUPT_SPOKEN_AUDIO_AND_MIX_WITH_OTHERS = "interruptSpokenAudioAndMixWithOthers"
    """
    Pause spoken audio content from other sessions when your app plays its audio.

    Available from iOS 9.0.
    """

    ALLOW_BLUETOOTH_A2DP = "allowBluetoothA2DP"
    """
    Stream audio from this session to Bluetooth devices
    that support the Advanced Audio Distribution Profile (A2DP).

    Note:
        Available from iOS 10.0.
    """

    ALLOW_AIRPLAY = "allowAirPlay"
    """
    Stream audio from this session to AirPlay devices.

    Note:
        Available from iOS 10.0.
    """

    OVERRIDE_MUTED_MICROPHONE_INTERRUPTION = "overrideMutedMicrophoneInterruption"
    """
    System interrupts the audio session when it mutes the built-in microphone.

    Note:
        Available from iOS 14.5.
    """


@dataclass
class IosRecorderConfiguration:
    """iOS specific configuration for recording."""

    options: list[IosAudioCategoryOption] = field(
        default_factory=lambda: [
            IosAudioCategoryOption.DEFAULT_TO_SPEAKER,
            IosAudioCategoryOption.ALLOW_BLUETOOTH,
            IosAudioCategoryOption.ALLOW_BLUETOOTH_A2DP,
        ]
    )
    """
    Optional audio behaviors.
    """

    manage_audio_session: bool = True
    """
    Whether to manage the shared AVAudioSession.

    Set this to `False` if another plugin is
    already managing the AVAudioSession.
    """


@dataclass
class InputDevice:
    """An audio input device."""

    id: str
    """The ID used to select the device on the platform."""

    label: str
    """The label text representation."""


@dataclass
class AudioRecorderConfiguration:
    """Recording configuration."""

    encoder: AudioEncoder = AudioEncoder.WAV
    """
    The requested output format through this given encoder.
    """

    suppress_noise: bool = False
    """
    The recorder will try to negate the input
    noise (if available on the device).

    Recording volume may be lowered by using this.
    """

    cancel_echo: bool = False
    """
    The recorder will try to reduce echo (if available on the device).

    Recording volume may be lowered by using this.
    """

    auto_gain: bool = False
    """
    The recorder will try to auto adjust recording volume in a
    limited range (if available on the device).

    Recording volume may be lowered by using this.
    """

    channels: int = 2
    """
    The numbers of channels for the recording.

    - `1` for mono
    - `2` for stereo

    Most platforms only accept at most 2 channels.
    """

    sample_rate: int = 44100
    """
    The sample rate for audio in samples per second if applicable.
    """

    bit_rate: ft.Number = 128000
    """
    The audio encoding bit rate in bits per second if applicable.
    """

    device: Optional[InputDevice] = None
    """
    The device to be used for recording.

    If `None`, default device will be selected.
    """

    android_configuration: AndroidRecorderConfiguration = field(
        default_factory=lambda: AndroidRecorderConfiguration()
    )
    """
    Android specific configuration.
    """

    ios_configuration: IosRecorderConfiguration = field(
        default_factory=lambda: IosRecorderConfiguration()
    )
    """
    iOS specific configuration.
    """
