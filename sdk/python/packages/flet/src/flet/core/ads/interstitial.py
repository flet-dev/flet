from typing import Any, Optional, Union

from flet.core.ads.base_ad import BaseAd
from flet.core.animation import AnimationValue
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.types import (
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet.utils import deprecated


@deprecated(
    reason="InterstitialAd control has been moved to a separate Python package: https://pypi.org/project/flet-ads. "
    + "Read more about this change in Flet blog: https://flet.dev/blog/flet-v-0-26-release-announcement",
    version="0.26.0",
    delete_version="0.29.0",
)
class InterstitialAd(BaseAd):
    """
    Displays a full screen interstitial ad.

    -----

    Online docs: https://flet.dev/docs/controls/interstitialad
    """

    def __init__(
        self,
        unit_id: str,
        on_load: OptionalControlEventCallable = None,
        on_error: OptionalControlEventCallable = None,
        on_open: OptionalControlEventCallable = None,
        on_close: OptionalControlEventCallable = None,
        on_impression: OptionalControlEventCallable = None,
        on_click: OptionalControlEventCallable = None,
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
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        BaseAd.__init__(
            self,
            unit_id=unit_id,
            on_load=on_load,
            on_error=on_error,
            on_open=on_open,
            on_close=on_close,
            on_impression=on_impression,
            on_click=on_click,
            #
            # ConstrainedControl
            #
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

    def _get_control_name(self):
        return "interstitial_ad"

    def show(self):
        self.invoke_method("show")
