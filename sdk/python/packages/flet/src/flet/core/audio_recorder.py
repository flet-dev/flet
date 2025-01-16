import json
from enum import Enum
from typing import Any, Optional

from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.types import OptionalEventCallable
from flet.utils import deprecated


class AudioRecorderState(Enum):
    STOPPED = "stopped"
    RECORDING = "recording"
    PAUSED = "paused"


class AudioRecorderStateChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.state: AudioRecorderState = AudioRecorderState(e.data)


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


@deprecated(
    reason="AudioRecorder control has been moved to a separate Python package: https://pypi.org/project/flet-audio-recorder. "
    + "Read more about this change in Flet blog: https://flet.dev/blog/flet-v-0-26-release-announcement",
    version="0.26.0",
    delete_version="0.29.0",
)
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
        on_state_changed: OptionalEventCallable[AudioRecorderStateChangeEvent] = None,
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
        self.__on_state_changed = EventHandler(
            lambda e: AudioRecorderStateChangeEvent(e)
        )
        self._add_event_handler("state_changed", self.__on_state_changed.get_handler())

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

    def start_recording(
        self, output_path: str = None, wait_timeout: Optional[float] = 10
    ) -> bool:
        assert (
            self.page.web or output_path
        ), "output_path must be provided when not on web"
        started = self.invoke_method(
            "start_recording",
            {"outputPath": output_path},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return started == "true"

    async def start_recording_async(
        self, output_path: str = None, wait_timeout: Optional[float] = 10
    ) -> bool:
        assert (
            self.page.web or output_path
        ), "output_path must be provided when not on web"
        started = await self.invoke_method_async(
            "start_recording",
            {"outputPath": output_path},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return started == "true"

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
        return self.invoke_method(
            "stop_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    async def stop_recording_async(
        self, wait_timeout: Optional[float] = 10
    ) -> Optional[str]:
        return await self.invoke_method_async(
            "stop_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    def cancel_recording(self, wait_timeout: Optional[float] = 5) -> None:
        self.invoke_method(
            "cancel_recording",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    def resume_recording(self):
        self.invoke_method("resume_recording")

    def pause_recording(self):
        self.invoke_method("pause_recording")

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

    async def get_input_devices_async(self, wait_timeout: Optional[float] = 5) -> dict:
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
        self._set_enum_attr("audioEncoder", value, AudioEncoder)

    # suppress_noise
    @property
    def suppress_noise(self) -> bool:
        return self._get_attr("suppressNoise", data_type="bool", def_value=False)

    @suppress_noise.setter
    def suppress_noise(self, value: Optional[bool]):
        self._set_attr("suppressNoise", value)

    # cancel_echo
    @property
    def cancel_echo(self) -> bool:
        return self._get_attr("cancelEcho", data_type="bool", def_value=False)

    @cancel_echo.setter
    def cancel_echo(self, value: Optional[bool]):
        self._set_attr("cancelEcho", value)

    # auto_gain
    @property
    def auto_gain(self) -> bool:
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
        return self.__on_state_changed.handler

    @on_state_changed.setter
    def on_state_changed(
        self, handler: OptionalEventCallable[AudioRecorderStateChangeEvent]
    ):
        self.__on_state_changed.handler = handler
