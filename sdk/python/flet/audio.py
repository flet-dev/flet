import dataclasses
import json
import threading
from enum import Enum
from typing import Any, Dict, List, Optional

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class ReleaseMode(Enum):
    RELEASE = "release"
    LOOP = "loop"
    STOP = "stop"


@dataclasses.dataclass
class AudioMethodCall:
    i: int
    n: str
    p: List[str]


@dataclasses.dataclass
class AudioMethodResults:
    i: int
    r: Optional[str]
    e: Optional[str]


class Audio(Control):
    """
    A control to simultaneously play multiple audio files. Works on macOS, Linux, Windows, iOS, Android and web. Based on audioplayers Flutter widget (https://pub.dev/packages/audioplayers).

    Audio control is non-visual and should be added to `page.overlay` list.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        audio1 = ft.Audio(
            src="https://luan.xyz/files/audio/ambient_c_motion.mp3", autoplay=True
        )
        page.overlay.append(audio1)
        page.add(
            ft.Text("This is an app with background audio."),
            ft.ElevatedButton("Stop playing", on_click=lambda _: audio1.pause()),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/audio
    """
    def __init__(
        self,
        src: Optional[str] = None,
        ref: Optional[Ref] = None,
        data: Any = None,
        # specific
        src_base64: Optional[str] = None,
        autoplay: Optional[bool] = None,
        volume: OptionalNumber = None,
        balance: OptionalNumber = None,
        playback_rate: OptionalNumber = None,
        release_mode: Optional[ReleaseMode] = None,
        on_loaded=None,
        on_duration_changed=None,
        on_state_changed=None,
        on_position_changed=None,
        on_seek_complete=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.__call_counter = 0
        self.__calls: Dict[int, threading.Event] = {}
        self.__results: Dict[threading.Event, tuple[Optional[str], Optional[str]]] = {}
        self._add_event_handler("result", self._on_result)
        self.src = src
        self.src_base64 = src_base64
        self.autoplay = autoplay
        self.volume = volume
        self.balance = balance
        self.playback_rate = playback_rate
        self.release_mode = release_mode
        self.on_loaded = on_loaded
        self.on_duration_changed = on_duration_changed
        self.on_state_changed = on_state_changed
        self.on_position_changed = on_position_changed
        self.on_seek_complete = on_seek_complete

    def _get_control_name(self):
        return "audio"

    def play(self):
        self._call_method("play", params=[], wait_for_result=False)

    def pause(self):
        self._call_method("pause", params=[], wait_for_result=False)

    def resume(self):
        self._call_method("resume", params=[], wait_for_result=False)

    def release(self):
        self._call_method("release", params=[], wait_for_result=False)

    def seek(self, position_milliseconds: int):
        self._call_method(
            "seek", params=[str(position_milliseconds)], wait_for_result=False
        )

    def get_duration(self) -> Optional[int]:
        sr = self._call_method("get_duration", [])
        return int(sr) if sr else None

    def get_current_position(self) -> Optional[int]:
        sr = self._call_method("get_current_position", [])
        return int(sr) if sr else None

    def _call_method(self, name: str, params: List[str], wait_for_result=True) -> Any:
        m = AudioMethodCall(i=self.__call_counter, n=name, p=params)
        self.__call_counter += 1
        self._set_attr_json("method", m)

        evt: Optional[threading.Event] = None
        if wait_for_result:
            evt = threading.Event()
            self.__calls[m.i] = evt
        self.update()

        if not wait_for_result:
            return

        assert evt is not None
        if not evt.wait(5):
            del self.__calls[m.i]
            raise Exception(f"Timeout waiting for Audio.{name}({params}) method call")
        result, err = self.__results.pop(evt)
        if err != None:
            raise Exception(err)
        if result == None:
            return None
        return json.loads(result)

    def _on_result(self, e):
        d = json.loads(e.data)
        result = AudioMethodResults(**d)
        evt = self.__calls.pop(result.i, None)
        if evt == None:
            return
        self.__results[evt] = (result.r, result.e)
        evt.set()

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value):
        self._set_attr("src", value)

    # src_base64
    @property
    def src_base64(self):
        return self._get_attr("srcBase64")

    @src_base64.setter
    def src_base64(self, value):
        self._set_attr("srcBase64", value)

    # autoplay
    @property
    def autoplay(self) -> Optional[bool]:
        return self._get_attr("autoplay", data_type="bool", def_value=False)

    @autoplay.setter
    @beartype
    def autoplay(self, value: Optional[bool]):
        self._set_attr("autoplay", value)

    # volume
    @property
    def volume(self) -> OptionalNumber:
        return self._get_attr("volume")

    @volume.setter
    @beartype
    def volume(self, value: OptionalNumber):
        if value is None or (value >= 0 and value <= 1):
            self._set_attr("volume", value)

    # balance
    @property
    def balance(self) -> OptionalNumber:
        return self._get_attr("balance")

    @balance.setter
    @beartype
    def balance(self, value: OptionalNumber):
        if value is None or (value >= -1 and value <= 1):
            self._set_attr("balance", value)

    # playback_rate
    @property
    def playback_rate(self) -> OptionalNumber:
        return self._get_attr("playbackRate")

    @playback_rate.setter
    @beartype
    def playback_rate(self, value: OptionalNumber):
        if value is None or (value >= 0 and value <= 2):
            self._set_attr("playbackRate", value)

    # release_mode
    @property
    def release_mode(self):
        return self._get_attr("releaseMode")

    @release_mode.setter
    @beartype
    def release_mode(self, value: Optional[ReleaseMode]):
        self._set_attr("releaseMode", value.value if value is not None else None)

    # on_loaded
    @property
    def on_loaded(self):
        return self._get_event_handler("loaded")

    @on_loaded.setter
    def on_loaded(self, handler):
        self._add_event_handler("loaded", handler)

    # on_duration_changed
    @property
    def on_duration_changed(self):
        return self._get_event_handler("duration_changed")

    @on_duration_changed.setter
    def on_duration_changed(self, handler):
        self._add_event_handler("duration_changed", handler)

    # on_state_changed
    @property
    def on_state_changed(self):
        return self._get_event_handler("state_changed")

    @on_state_changed.setter
    def on_state_changed(self, handler):
        self._add_event_handler("state_changed", handler)

    # on_position_changed
    @property
    def on_position_changed(self):
        return self._get_event_handler("position_changed")

    @on_position_changed.setter
    def on_position_changed(self, handler):
        self._add_event_handler("position_changed", handler)
        if handler is not None:
            self._set_attr("onPositionChanged", True)
        else:
            self._set_attr("onPositionChanged", None)

    # on_seek_complete
    @property
    def on_seek_complete(self):
        return self._get_event_handler("seek_complete")

    @on_seek_complete.setter
    def on_seek_complete(self, handler):
        self._add_event_handler("seek_complete", handler)
