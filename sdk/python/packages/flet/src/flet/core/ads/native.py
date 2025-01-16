import dataclasses
from enum import Enum
from typing import Any, Optional, Union

from flet.core.ads.base_ad import BaseAd
from flet.core.animation import AnimationValue
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.types import OffsetValue, ResponsiveNumber, RotateValue, ScaleValue


class NativeAdTemplateType(Enum):
    SMALL = "small"
    MEDIUM = "medium"


class NativeTemplateFontStyle(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    MONOSPACE = "monospace"


@dataclasses.dataclass
class NativeAdTemplateTextStyle:
    size: OptionalNumber = dataclasses.field(default=None)
    text_color: Optional[str] = dataclasses.field(default=None)
    bgcolor: Optional[str] = dataclasses.field(default=None)
    style: Optional[NativeTemplateFontStyle] = dataclasses.field(default=None)


@dataclasses.dataclass
class NativeAdTemplateStyle:
    template_type: Optional[NativeAdTemplateType] = dataclasses.field(default=None)
    main_bgcolor: Optional[str] = dataclasses.field(default=None)
    corner_radius: OptionalNumber = dataclasses.field(default=None)
    call_to_action_text_style: Optional[NativeAdTemplateTextStyle] = dataclasses.field(
        default=None
    )
    primary_text_style: Optional[NativeAdTemplateTextStyle] = dataclasses.field(
        default=None
    )
    secondary_text_style: Optional[NativeAdTemplateTextStyle] = dataclasses.field(
        default=None
    )
    tertiary_text_style: Optional[NativeAdTemplateTextStyle] = dataclasses.field(
        default=None
    )


class NativeAd(BaseAd):
    """
    TBA

    -----

    Online docs: https://flet.dev/docs/controls/nativead
    """

    def __init__(
        self,
        unit_id: str = None,
        factory_id: str = None,
        template_style: NativeAdTemplateStyle = None,
        on_load=None,
        on_error=None,
        on_open=None,
        on_close=None,
        on_impression=None,
        on_click=None,
        on_will_dismiss=None,
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
        on_animation_end=None,
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
            on_will_dismiss=on_will_dismiss,
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

        self.template_style = template_style
        self.factory_id = factory_id

    def _get_control_name(self):
        return "native_ad"

    def before_update(self):
        super().before_update()
        self._set_attr_json("templateStyle", self.__template_style)

    @property
    def template_style(self):
        return self.__template_style

    @template_style.setter
    def template_style(self, value):
        self.__template_style = value

    # factory_id
    @property
    def factory_id(self) -> Optional[str]:
        return self._get_attr("factoryId")

    @factory_id.setter
    def factory_id(self, value: Optional[str]):
        self._set_attr("factoryId", value)
