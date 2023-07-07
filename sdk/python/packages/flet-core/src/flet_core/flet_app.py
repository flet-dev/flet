from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, OffsetValue, RotateValue, ScaleValue

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class FletApp(ConstrainedControl):
    def __init__(
        self,
        url: Optional[str] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        reconnect_interval_ms: Optional[int] = None,
        reconnect_timeout_ms: Optional[int] = None,
        on_error=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.url = url
        self.reconnect_interval_ms = reconnect_interval_ms
        self.reconnect_timeout_ms = reconnect_timeout_ms
        self.on_error = on_error

    def _get_control_name(self):
        return "fletapp"

    # url
    @property
    def url(self):
        return self._get_attr("url")

    @url.setter
    def url(self, value):
        self._set_attr("url", value)

    # reconnect_interval_ms
    @property
    def reconnect_interval_ms(self) -> Optional[int]:
        return self._get_attr("reconnectIntervalMs")

    @reconnect_interval_ms.setter
    def reconnect_interval_ms(self, value: Optional[int]):
        self._set_attr("reconnectIntervalMs", value)

    # reconnect_timeout_ms
    @property
    def reconnect_timeout_ms(self) -> Optional[int]:
        return self._get_attr("reconnectTimeoutMs")

    @reconnect_timeout_ms.setter
    def reconnect_timeout_ms(self, value: Optional[int]):
        self._set_attr("reconnectTimeoutMs", value)

    # on_error
    @property
    def on_error(self):
        return self._get_event_handler("error")

    @on_error.setter
    def on_error(self, handler):
        self._add_event_handler("error", handler)
