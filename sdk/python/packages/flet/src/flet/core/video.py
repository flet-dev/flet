import dataclasses
from enum import Enum
from typing import Any, Dict, List, Optional, Union, cast

from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.box import FilterQuality
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    ImageFit,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
)
from flet.utils import deprecated


class PlaylistMode(Enum):
    NONE = "none"
    SINGLE = "single"
    LOOP = "loop"


@dataclasses.dataclass
class VideoMedia:
    resource: Optional[str] = dataclasses.field(default=None)
    http_headers: Optional[Dict[str, str]] = dataclasses.field(default=None)
    extras: Optional[Dict[str, str]] = dataclasses.field(default=None)


@dataclasses.dataclass
class VideoConfiguration:
    output_driver: Optional[str] = dataclasses.field(default=None)
    hardware_decoding_api: Optional[str] = dataclasses.field(default=None)
    enable_hardware_acceleration: Optional[bool] = dataclasses.field(default=None)


@dataclasses.dataclass
class VideoSubtitleConfiguration:
    src: Optional[str] = dataclasses.field(default=None)
    title: Optional[str] = dataclasses.field(default=None)
    language: Optional[str] = dataclasses.field(default=None)
    text_style: Optional[TextStyle] = dataclasses.field(default=None)
    text_scale_factor: Optional[OptionalNumber] = dataclasses.field(default=None)
    text_align: Optional[TextAlign] = dataclasses.field(default=None)
    padding: Optional[PaddingValue] = dataclasses.field(default=None)
    visible: Optional[bool] = dataclasses.field(default=None)


@deprecated(
    reason="Video control has been moved to a separate Python package: https://pypi.org/project/flet-video. "
    + "Read more about this change in Flet blog: https://flet.dev/blog/flet-v-0-26-release-announcement",
    version="0.26.0",
    delete_version="0.29.0",
)
class Video(ConstrainedControl):
    """
    A control that displays a video from a playlist.

    -----

    Online docs: https://flet.dev/docs/controls/video
    """

    def __init__(
        self,
        playlist: Optional[List[VideoMedia]] = None,
        title: Optional[str] = None,
        fit: Optional[ImageFit] = None,
        fill_color: Optional[ColorValue] = None,
        wakelock: Optional[bool] = None,
        autoplay: Optional[bool] = None,
        show_controls: Optional[bool] = None,
        muted: Optional[bool] = None,
        playlist_mode: Optional[PlaylistMode] = None,
        shuffle_playlist: Optional[bool] = None,
        volume: OptionalNumber = None,
        playback_rate: OptionalNumber = None,
        alignment: Optional[Alignment] = None,
        filter_quality: Optional[FilterQuality] = None,
        pause_upon_entering_background_mode: Optional[bool] = None,
        resume_upon_entering_foreground_mode: Optional[bool] = None,
        aspect_ratio: OptionalNumber = None,
        pitch: OptionalNumber = None,
        configuration: Optional[VideoConfiguration] = None,
        subtitle_configuration: Optional[VideoSubtitleConfiguration] = None,
        on_loaded: OptionalControlEventCallable = None,
        on_enter_fullscreen: OptionalControlEventCallable = None,
        on_exit_fullscreen: OptionalControlEventCallable = None,
        on_error: OptionalControlEventCallable = None,
        on_completed: OptionalControlEventCallable = None,
        on_track_changed: OptionalControlEventCallable = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__playlist = playlist or []
        self.subtitle_configuration = subtitle_configuration
        self.configuration = configuration
        self.fit = fit
        self.pitch = pitch
        self.fill_color = fill_color
        self.volume = volume
        self.playback_rate = playback_rate
        self.alignment = alignment
        self.wakelock = wakelock
        self.autoplay = autoplay
        self.show_controls = show_controls
        self.shuffle_playlist = shuffle_playlist
        self.muted = muted
        self.title = title
        self.filter_quality = filter_quality
        self.playlist_mode = playlist_mode
        self.pause_upon_entering_background_mode = pause_upon_entering_background_mode
        self.resume_upon_entering_foreground_mode = resume_upon_entering_foreground_mode
        self.on_enter_fullscreen = on_enter_fullscreen
        self.on_exit_fullscreen = on_exit_fullscreen
        self.on_loaded = on_loaded
        self.on_error = on_error
        self.on_completed = on_completed
        self.on_track_changed = on_track_changed

    def _get_control_name(self):
        return "video"

    def before_update(self):
        super().before_update()
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("playlist", self.__playlist if self.__playlist else None)
        if isinstance(self.__subtitle_configuration, VideoSubtitleConfiguration):
            self._set_attr_json("subtitleConfiguration", self.__subtitle_configuration)

        if isinstance(self.__configuration, VideoConfiguration):
            self._set_attr_json("configuration", self.__configuration)

    def play(self):
        self.invoke_method("play")

    def pause(self):
        self.invoke_method("pause")

    def play_or_pause(self):
        self.invoke_method("play_or_pause")

    def stop(self):
        self.invoke_method("stop")

    def next(self):
        self.invoke_method("next")

    def previous(self):
        self.invoke_method("previous")

    def seek(self, position_milliseconds: int):
        self.invoke_method("seek", {"position": str(position_milliseconds)})

    def jump_to(self, media_index: int):
        assert self.__playlist[media_index], "media_index is out of range"
        if media_index < 0:
            # dart doesn't support negative indexes
            media_index = len(self.__playlist) + media_index
        self.invoke_method("jump_to", {"media_index": str(media_index)})

    def playlist_add(self, media: VideoMedia):
        assert media.resource, "media has no resource"
        self.invoke_method(
            "playlist_add",
            {
                "resource": media.resource,
                "http_headers": str(media.http_headers or {}),
                "extras": str(media.extras or {}),
            },
        )
        self.__playlist.append(media)

    def playlist_remove(self, media_index: int):
        assert self.__playlist[media_index], "index out of range"
        self.invoke_method("playlist_remove", {"media_index": str(media_index)})
        self.__playlist.pop(media_index)

    def is_playing(self, wait_timeout: Optional[float] = 5) -> bool:
        playing = self.invoke_method(
            "is_playing",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return playing == "true"

    async def is_playing_async(self, wait_timeout: Optional[float] = 5) -> bool:
        playing = await self.invoke_method_async(
            "is_playing",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return playing == "true"

    def is_completed(self, wait_timeout: Optional[float] = 5) -> bool:
        completed = self.invoke_method(
            "is_completed",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return completed == "true"

    async def is_completed_async(self, wait_timeout: Optional[float] = 5) -> bool:
        completed = await self.invoke_method_async(
            "is_completed",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return completed == "true"

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

    # playlist
    @property
    def playlist(self) -> Optional[List[VideoMedia]]:
        return self.__playlist

    # fit
    @property
    def fit(self) -> Optional[ImageFit]:
        return self.__fit

    @fit.setter
    def fit(self, value: Optional[ImageFit]):
        self.__fit = value
        self._set_attr("fit", value.value if isinstance(value, ImageFit) else value)

    # subtitle_configuration
    @property
    def subtitle_configuration(self) -> Optional[VideoSubtitleConfiguration]:
        return self.__subtitle_configuration

    @subtitle_configuration.setter
    def subtitle_configuration(self, value: Optional[VideoSubtitleConfiguration]):
        self.__subtitle_configuration = value

    # configuration
    @property
    def configuration(self) -> Optional[VideoConfiguration]:
        return self.__configuration

    @configuration.setter
    def configuration(self, value: Optional[VideoConfiguration]):
        self.__configuration = value

    # fill_color
    @property
    def fill_color(self) -> Optional[ColorValue]:
        return self.__fill_color

    @fill_color.setter
    def fill_color(self, value: Optional[ColorValue]):
        self.__fill_color = value
        self._set_enum_attr("fillColor", value, ColorEnums)

    # wakelock
    @property
    def wakelock(self) -> bool:
        return self._get_attr("wakelock", data_type="bool", def_value=True)

    @wakelock.setter
    def wakelock(self, value: Optional[bool]):
        self._set_attr("wakelock", value)

    # autoplay
    @property
    def autoplay(self) -> bool:
        return self._get_attr("autoPlay", data_type="bool", def_value=False)

    @autoplay.setter
    def autoplay(self, value: Optional[bool]):
        self._set_attr("autoPlay", value)

    # muted
    @property
    def muted(self) -> bool:
        return self._get_attr("muted", data_type="bool", def_value=False)

    @muted.setter
    def muted(self, value: Optional[bool]):
        self._set_attr("muted", value)

    # shuffle_playlist
    @property
    def shuffle_playlist(self) -> bool:
        return self._get_attr("shufflePlaylist", data_type="bool", def_value=False)

    @shuffle_playlist.setter
    def shuffle_playlist(self, value: Optional[bool]):
        self._set_attr("shufflePlaylist", value)

    # show_controls
    @property
    def show_controls(self) -> bool:
        return self._get_attr("showControls", data_type="bool", def_value=True)

    @show_controls.setter
    def show_controls(self, value: Optional[bool]):
        self._set_attr("showControls", value)

    # pitch
    @property
    def pitch(self) -> OptionalNumber:
        return self._get_attr("pitch", data_type="float")

    @pitch.setter
    def pitch(self, value: OptionalNumber):
        self._set_attr("pitch", value)

    # volume
    @property
    def volume(self) -> OptionalNumber:
        return self._get_attr("volume", data_type="float")

    @volume.setter
    def volume(self, value: OptionalNumber):
        assert value is None or 0 <= value <= 100, "volume must be between 0 and 100"
        self._set_attr("volume", value)

    # playback_rate
    @property
    def playback_rate(self) -> OptionalNumber:
        return self._get_attr("playbackRate", data_type="float")

    @playback_rate.setter
    def playback_rate(self, value: OptionalNumber):
        self._set_attr("playbackRate", value)

    # title
    @property
    def title(self) -> Optional[str]:
        return self._get_attr("title")

    @title.setter
    def title(self, value: Optional[str]):
        self._set_attr("title", value)

    # pause_upon_entering_background_mode
    @property
    def pause_upon_entering_background_mode(self) -> bool:
        return cast(
            bool,
            self._get_attr(
                "pauseUponEnteringBackgroundMode", data_type="bool", def_value=True
            ),
        )

    @pause_upon_entering_background_mode.setter
    def pause_upon_entering_background_mode(self, value: Optional[bool]):
        self._set_attr("pauseUponEnteringBackgroundMode", value)

    # resume_upon_entering_foreground_mode
    @property
    def resume_upon_entering_foreground_mode(self) -> bool:
        return cast(
            bool,
            self._get_attr(
                "resumeUponEnteringForegroundMode", data_type="bool", def_value=False
            ),
        )

    @resume_upon_entering_foreground_mode.setter
    def resume_upon_entering_foreground_mode(self, value: Optional[bool]):
        self._set_attr("resumeUponEnteringForegroundMode", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # filter_quality
    @property
    def filter_quality(self) -> Optional[FilterQuality]:
        return self.__filter_quality

    @filter_quality.setter
    def filter_quality(self, value: Optional[FilterQuality]):
        self.__filter_quality = value
        self._set_enum_attr("filterQuality", value, FilterQuality)

    # playlist_mode
    @property
    def playlist_mode(self) -> Optional[PlaylistMode]:
        return self.__playlist_mode

    @playlist_mode.setter
    def playlist_mode(self, value: Optional[PlaylistMode]):
        self.__playlist_mode = value
        self._set_enum_attr("playlistMode", value, PlaylistMode)

    # on_enter_fullscreen
    @property
    def on_enter_fullscreen(self):
        return self._get_event_handler("enter_fullscreen")

    @on_enter_fullscreen.setter
    def on_enter_fullscreen(self, handler: OptionalControlEventCallable):
        self._add_event_handler("enter_fullscreen", handler)
        self._set_attr("onEnterFullscreen", True if handler is not None else None)

    # on_exit_fullscreen
    @property
    def on_exit_fullscreen(self) -> OptionalControlEventCallable:
        return self._get_event_handler("exit_fullscreen")

    @on_exit_fullscreen.setter
    def on_exit_fullscreen(self, handler: OptionalControlEventCallable):
        self._add_event_handler("exit_fullscreen", handler)
        self._set_attr("onExitFullscreen", True if handler is not None else None)

    # on_loaded
    @property
    def on_loaded(self) -> OptionalControlEventCallable:
        return self._get_event_handler("loaded")

    @on_loaded.setter
    def on_loaded(self, handler: OptionalControlEventCallable):
        self._set_attr("onLoaded", True if handler is not None else None)
        self._add_event_handler("loaded", handler)

    # on_error
    @property
    def on_error(self) -> OptionalControlEventCallable:
        return self._get_event_handler("error")

    @on_error.setter
    def on_error(self, handler: OptionalControlEventCallable):
        self._set_attr("onError", True if handler is not None else None)
        self._add_event_handler("error", handler)

    # on_completed
    @property
    def on_completed(self) -> OptionalControlEventCallable:
        return self._get_event_handler("completed")

    @on_completed.setter
    def on_completed(self, handler: OptionalControlEventCallable):
        self._set_attr("onCompleted", True if handler is not None else None)
        self._add_event_handler("completed", handler)

    # on_track_changed
    @property
    def on_track_changed(self) -> OptionalControlEventCallable:
        return self._get_event_handler("track_changed")

    @on_track_changed.setter
    def on_track_changed(self, handler: OptionalControlEventCallable):
        self._set_attr("onTrackChanged", True if handler is not None else None)
        self._add_event_handler("track_changed", handler)
