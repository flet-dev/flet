import json
from enum import Enum
from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.utils import deprecated


class AudioEncoder(Enum):
    AACLC = "aacLc"
    AACELD = "aacEld"
    AACHE = "aacHe"
    AMRNB = "amrNb"
    AMRWB = "amrWb"
    OPUS = "opus"
    FLAC = "flac"
    WAV = "wav"
    PCM16BITS = "pcm16bits"


class AudioRecorder(Control):
    """
    A control that allows you to record audio from your device.

    -----

    Online docs: https://flet.dev/docs/controls/audiorecorder
    """

    def __init__(
        self,
        audio_encoder: Optional[AudioEncoder] = None,
        suppress_noise: Optional[bool] = None,
        cancel_echo: Optional[bool] = None,
        auto_gain: Optional[bool] = None,
        channels_num: OptionalNumber = None,
        sample_rate: OptionalNumber = None,
        bit_rate: OptionalNumber = None,
        on_state_changed=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )
        self.audio_encoder = audio_encoder
        self.suppress_noise = suppress_noise
        self.cancel_echo = cancel_echo
        self.auto_gain = auto_gain
        self.channels_num = channels_num
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.on_state_changed = on_state_changed

    def _get_control_name(self):
        return "audiorecorder"

    def start_recording(self, output_path: str = None):
        if not self.page.web and not output_path:
            raise ValueError("output_path must be provided when not on web!")
        self.invoke_method("start_recording", {"outputPath": output_path})

    @deprecated(
        reason="Use start_recording() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def start_recording_async(self, output_path: str):
        self.start_recording(output_path)

    def is_recording(self, wait_timeout: Optional[float] = 5) -> bool:
        recording = self.invoke_method(
            "is_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return recording == "true"

    async def is_recording_async(self, wait_timeout: Optional[float] = 5) -> bool:
        recording = await self.invoke_method_async(
            "is_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return recording == "true"

    def stop_recording(self, wait_timeout: Optional[float] = 5) -> Optional[str]:
        out = self.invoke_method(
            "stop_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return out if out != "null" else None

    async def stop_recording_async(
        self, wait_timeout: Optional[float] = 10
    ) -> Optional[str]:
        out = await self.invoke_method_async(
            "stop_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return out if out != "null" else None

    def resume_recording(self):
        self.invoke_method("resume_recording")

    @deprecated(
        reason="Use resume_recording() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def resume_recording_async(self):
        self.resume_recording()

    def pause_recording(self):
        self.invoke_method("pause_recording")

    @deprecated(
        reason="Use pause_recording() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def pause_recording_async(self):
        self.pause_recording()

    def is_paused(self, wait_timeout: Optional[float] = 5) -> bool:
        paused = self.invoke_method(
            "is_paused",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return paused == "true"

    async def is_paused_async(self, wait_timeout: Optional[float] = 5) -> bool:
        supported = await self.invoke_method_async(
            "is_paused",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return supported == "true"

    def is_supported_encoder(
        self, encoder: AudioEncoder, wait_timeout: Optional[float] = 5
    ) -> bool:
        supported = self.invoke_method(
            "is_supported_encoder",
            {
                "encoder": (
                    encoder.value if isinstance(encoder, AudioEncoder) else encoder
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return supported == "true"

    async def is_supported_encoder_async(
        self, encoder: AudioEncoder, wait_timeout: Optional[float] = 5
    ) -> bool:
        supported = await self.invoke_method_async(
            "is_supported_encoder",
            {
                "encoder": (
                    encoder.value if isinstance(encoder, AudioEncoder) else encoder
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return supported == "true"

    def get_input_devices(self, wait_timeout: Optional[float] = 5) -> dict:
        devices = self.invoke_method(
            "get_input_devices",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return json.loads(devices)

    async def get_input_devices_async(self, wait_timeout: Optional[float] = 5) -> bool:
        devices = await self.invoke_method_async(
            "get_input_devices",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return json.loads(devices)

    def has_permission(self, wait_timeout: Optional[float] = 10) -> bool:
        p = self.invoke_method(
            "has_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return p == "true"

    async def has_permission_async(self, wait_timeout: Optional[float] = 10) -> bool:
        p = await self.invoke_method_async(
            "has_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return p == "true"

    # audio_encoder
    @property
    def audio_encoder(self):
        return self._get_attr("audioEncoder")

    @audio_encoder.setter
    def audio_encoder(self, value: Optional[AudioEncoder]):
        self._set_attr(
            "audioEncoder", value.value if isinstance(value, AudioEncoder) else value
        )

    # suppress_noise
    @property
    def suppress_noise(self) -> Optional[bool]:
        return self._get_attr("suppressNoise", data_type="bool", def_value=False)

    @suppress_noise.setter
    def suppress_noise(self, value: Optional[bool]):
        self._set_attr("suppressNoise", value)

    # cancel_echo
    @property
    def cancel_echo(self) -> Optional[bool]:
        return self._get_attr("cancelEcho", data_type="bool", def_value=False)

    @cancel_echo.setter
    def cancel_echo(self, value: Optional[bool]):
        self._set_attr("cancelEcho", value)

    # auto_gain
    @property
    def auto_gain(self) -> Optional[bool]:
        return self._get_attr("autoGain", data_type="bool", def_value=False)

    @auto_gain.setter
    def auto_gain(self, value: Optional[bool]):
        self._set_attr("autoGain", value)

    # bit_rate
    @property
    def bit_rate(self) -> OptionalNumber:
        return self._get_attr("bitRate")

    @bit_rate.setter
    def bit_rate(self, value: OptionalNumber):
        self._set_attr("bitRate", value)

    # sample_rate
    @property
    def sample_rate(self) -> OptionalNumber:
        return self._get_attr("sampleRate")

    @sample_rate.setter
    def sample_rate(self, value: OptionalNumber):
        self._set_attr("sampleRate", value)

    # channels_num
    @property
    def channels_num(self) -> OptionalNumber:
        return self._get_attr("channels")

    @channels_num.setter
    def channels_num(self, value: OptionalNumber):
        if value is None or value in (1, 2):
            self._set_attr("channels", value)

    # on_state_changed
    @property
    def on_state_changed(self):
        return self._get_event_handler("state_changed")

    @on_state_changed.setter
    def on_state_changed(self, handler):
        self._add_event_handler("state_changed", handler)
