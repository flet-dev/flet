from enum import Enum
from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.utils import deprecated


class ReleaseMode(Enum):
    RELEASE = "release"
    LOOP = "loop"
    STOP = "stop"


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
        self.invoke_method("play")

    @deprecated(
        reason="Use play() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def play_async(self):
        self.play()

    def pause(self):
        self.invoke_method("pause")

    @deprecated(
        reason="Use pause() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def pause_async(self):
        self.pause()

    def resume(self):
        self.invoke_method("resume")

    @deprecated(
        reason="Use resume() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def resume_async(self):
        self.resume()

    def release(self):
        self.invoke_method("release")

    @deprecated(
        reason="Use release() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def release_async(self):
        self.release()

    def seek(self, position_milliseconds: int):
        self.invoke_method("seek", {"position": str(position_milliseconds)})

    @deprecated(
        reason="Use seek() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def seek_async(self, position_milliseconds: int):
        self.seek(position_milliseconds)

    def get_duration(self, wait_timeout: Optional[float] = 5) -> Optional[int]:
        sr = self.invoke_method(
            "get_duration",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return int(sr) if sr else None

    async def get_duration_async(
        self, wait_timeout: Optional[float] = 5
    ) -> Optional[int]:
        sr = await self.invoke_method_async(
            "get_duration",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return int(sr) if sr else None

    def get_current_position(self, wait_timeout: Optional[float] = 5) -> Optional[int]:
        sr = self.invoke_method(
            "get_current_position",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return int(sr) if sr else None

    async def get_current_position_async(
        self, wait_timeout: Optional[float] = 5
    ) -> Optional[int]:
        sr = await self.invoke_method_async(
            "get_current_position",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return int(sr) if sr else None

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
    def autoplay(self, value: Optional[bool]):
        self._set_attr("autoplay", value)

    # volume
    @property
    def volume(self) -> OptionalNumber:
        return self._get_attr("volume")

    @volume.setter
    def volume(self, value: OptionalNumber):
        if value is None or (0 <= value <= 1):
            self._set_attr("volume", value)

    # balance
    @property
    def balance(self) -> OptionalNumber:
        return self._get_attr("balance")

    @balance.setter
    def balance(self, value: OptionalNumber):
        if value is None or (-1 <= value <= 1):
            self._set_attr("balance", value)

    # playback_rate
    @property
    def playback_rate(self) -> OptionalNumber:
        return self._get_attr("playbackRate")

    @playback_rate.setter
    def playback_rate(self, value: OptionalNumber):
        if value is None or (0 <= value <= 2):
            self._set_attr("playbackRate", value)

    # release_mode
    @property
    def release_mode(self):
        return self._get_attr("releaseMode")

    @release_mode.setter
    def release_mode(self, value: Optional[ReleaseMode]):
        self._set_enum_attr("releaseMode", value, ReleaseMode)

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
