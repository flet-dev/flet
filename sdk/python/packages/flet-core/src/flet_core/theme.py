import dataclasses
from dataclasses import field
from enum import Enum, EnumMeta
from typing import Dict, List, Optional, Union
from warnings import warn

from flet_core.alignment import Alignment
from flet_core.border import BorderSide
from flet_core.border_radius import BorderRadius
from flet_core.buttons import ButtonStyle, OutlinedBorder
from flet_core.control import OptionalNumber
from flet_core.navigation_bar import NavigationBarLabelBehavior
from flet_core.navigation_rail import NavigationRailLabelType
from flet_core.padding import Padding
from flet_core.popup_menu_button import PopupMenuPosition
from flet_core.shadow import BoxShadow
from flet_core.snack_bar import DismissDirection, SnackBarBehavior
from flet_core.text_style import TextStyle
from flet_core.textfield import TextCapitalization
from flet_core.types import (
    Brightness,
    ClipBehavior,
    MarginValue,
    MaterialState,
    MouseCursor,
    OffsetValue,
    PaddingValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class ThemeVisualDensityDeprecated(EnumMeta):
    def __getattribute__(self, item):
        if item == "ADAPTIVEPLATFORMDENSITY":
            warn(
                "ADAPTIVEPLATFORMDENSITY is deprecated and will be removed in v1.0. "
                "Use ADAPTIVE_PLATFORM_DENSITY instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        return EnumMeta.__getattribute__(self, item)


class ThemeVisualDensity(Enum, metaclass=ThemeVisualDensityDeprecated):
    NONE = None
    STANDARD = "standard"
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    ADAPTIVEPLATFORMDENSITY = "adaptivePlatformDensity"
    ADAPTIVE_PLATFORM_DENSITY = "adaptivePlatformDensity"


PageTransitionString = Literal["fadeUpwards", "openUpwards", "zoom", "cupertino"]


class PageTransitionTheme(Enum):
    NONE = "none"
    FADE_UPWARDS = "fadeUpwards"
    OPEN_UPWARDS = "openUpwards"
    ZOOM = "zoom"
    CUPERTINO = "cupertino"


@dataclasses.dataclass
class PageTransitionsTheme:
    android: Optional[PageTransitionTheme] = field(default=None)
    ios: Optional[PageTransitionTheme] = field(default=None)
    linux: Optional[PageTransitionTheme] = field(default=None)
    macos: Optional[PageTransitionTheme] = field(default=None)
    windows: Optional[PageTransitionTheme] = field(default=None)


@dataclasses.dataclass
class ColorScheme:
    primary: Optional[str] = field(default=None)
    on_primary: Optional[str] = field(default=None)
    primary_container: Optional[str] = field(default=None)
    on_primary_container: Optional[str] = field(default=None)
    secondary: Optional[str] = field(default=None)
    on_secondary: Optional[str] = field(default=None)
    secondary_container: Optional[str] = field(default=None)
    on_secondary_container: Optional[str] = field(default=None)
    tertiary: Optional[str] = field(default=None)
    on_tertiary: Optional[str] = field(default=None)
    tertiary_container: Optional[str] = field(default=None)
    on_tertiary_container: Optional[str] = field(default=None)
    error: Optional[str] = field(default=None)
    on_error: Optional[str] = field(default=None)
    error_container: Optional[str] = field(default=None)
    on_error_container: Optional[str] = field(default=None)
    background: Optional[str] = field(default=None)
    on_background: Optional[str] = field(default=None)
    surface: Optional[str] = field(default=None)
    on_surface: Optional[str] = field(default=None)
    surface_variant: Optional[str] = field(default=None)
    on_surface_variant: Optional[str] = field(default=None)
    outline: Optional[str] = field(default=None)
    outline_variant: Optional[str] = field(default=None)
    shadow: Optional[str] = field(default=None)
    scrim: Optional[str] = field(default=None)
    inverse_surface: Optional[str] = field(default=None)
    on_inverse_surface: Optional[str] = field(default=None)
    inverse_primary: Optional[str] = field(default=None)
    surface_tint: Optional[str] = field(default=None)


@dataclasses.dataclass
class TextTheme:
    body_large: Optional[TextStyle] = field(default=None)
    body_medium: Optional[TextStyle] = field(default=None)
    body_small: Optional[TextStyle] = field(default=None)
    display_large: Optional[TextStyle] = field(default=None)
    display_medium: Optional[TextStyle] = field(default=None)
    display_small: Optional[TextStyle] = field(default=None)
    headline_large: Optional[TextStyle] = field(default=None)
    headline_medium: Optional[TextStyle] = field(default=None)
    headline_small: Optional[TextStyle] = field(default=None)
    label_large: Optional[TextStyle] = field(default=None)
    label_medium: Optional[TextStyle] = field(default=None)
    label_small: Optional[TextStyle] = field(default=None)
    title_large: Optional[TextStyle] = field(default=None)
    title_medium: Optional[TextStyle] = field(default=None)
    title_small: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class ScrollbarTheme:
    thumb_visibility: Union[None, bool, Dict[MaterialState, bool]] = field(default=None)
    thickness: Union[None, float, Dict[MaterialState, float]] = field(default=None)
    track_visibility: Union[None, bool, Dict[MaterialState, bool]] = field(default=None)
    radius: Optional[float] = field(default=None)
    thumb_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    track_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    track_border_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    cross_axis_margin: Optional[float] = field(default=None)
    main_axis_margin: Optional[float] = field(default=None)
    min_thumb_length: Optional[float] = field(default=None)
    interactive: Optional[bool] = field(default=None)


@dataclasses.dataclass
class TabsTheme:
    divider_color: Optional[str] = field(default=None)
    indicator_border_radius: Optional[BorderRadius] = field(default=None)
    indicator_border_side: Optional[BorderSide] = field(default=None)
    indicator_padding: PaddingValue = field(default=None)
    indicator_color: Optional[str] = field(default=None)
    indicator_tab_size: Optional[bool] = field(default=None)
    label_color: Optional[str] = field(default=None)
    unselected_label_color: Optional[str] = field(default=None)
    overlay_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, MaterialState], MouseCursor]
    ] = field(default=None)
    label_padding: PaddingValue = field(default=None)
    label_text_style: Optional[TextStyle] = field(default=None)
    unselected_label_text_style: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class SystemOverlayStyle:
    status_bar_color: Optional[str] = field(default=None)
    system_navigation_bar_color: Optional[str] = field(default=None)
    system_navigation_bar_divider_color: Optional[str] = field(default=None)
    enforce_system_navigation_bar_contrast: Optional[bool] = field(default=None)
    enforce_system_status_bar_contrast: Optional[bool] = field(default=None)
    system_navigation_bar_icon_brightness: Optional[Brightness] = field(default=None)
    status_bar_brightness: Optional[Brightness] = field(default=None)
    status_bar_icon_brightness: Optional[Brightness] = field(default=None)


@dataclasses.dataclass
class DialogTheme:
    bgcolor: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    icon_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    title_text_style: Optional[TextStyle] = field(default=None)
    content_text_style: Optional[TextStyle] = field(default=None)
    alignment: Optional[Alignment] = field(default=None)
    actions_padding: Optional[PaddingValue] = field(default=None)


@dataclasses.dataclass
class BottomSheetTheme:
    bgcolor: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    drag_handle_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    show_drag_handle: Optional[bool] = field(default=None)
    modal_bgcolor: Optional[str] = field(default=None)
    modal_elevation: OptionalNumber = field(default=None)
    clip_behavior: Optional[ClipBehavior] = field(default=None)


@dataclasses.dataclass
class CardTheme:
    color: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    clip_behavior: Optional[ClipBehavior] = field(default=None)
    margin: MarginValue = field(default=None)


@dataclasses.dataclass
class ChipTheme:
    # color: Optional[str] = field(default=None)
    bgcolor: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    disabled_color: Optional[str] = field(default=None)
    selected_color: Optional[str] = field(default=None)
    checkmark_color: Optional[str] = field(default=None)
    delete_icon_color: Optional[str] = field(default=None)
    secondary_selected_color: Optional[str] = field(default=None)
    selected_shadow_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    click_elevation: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    padding: PaddingValue = field(default=None)
    label_padding: PaddingValue = field(default=None)
    label_text_style: Optional[TextStyle] = field(default=None)
    secondary_label_text_style: Optional[TextStyle] = field(default=None)
    border_side: Optional[BorderSide] = field(default=None)
    brightness: Optional[Brightness] = field(default=None)
    show_checkmark: Optional[bool] = field(default=None)


@dataclasses.dataclass
class FloatingActionButtonTheme:
    bgcolor: Optional[str] = field(default=None)
    hover_color: Optional[str] = field(default=None)
    focus_color: Optional[str] = field(default=None)
    foreground_color: Optional[str] = field(default=None)
    splash_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    focus_elevation: OptionalNumber = field(default=None)
    hover_elevation: OptionalNumber = field(default=None)
    highlight_elevation: OptionalNumber = field(default=None)
    disabled_elevation: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    enable_feedback: Optional[bool] = field(default=None)
    extended_padding: PaddingValue = field(default=None)
    extended_text_style: Optional[TextStyle] = field(default=None)
    extended_icon_label_spacing: OptionalNumber = field(default=None)


@dataclasses.dataclass
class NavigationRailTheme:
    bgcolor: Optional[str] = field(default=None)
    indicator_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    indicator_shape: Optional[OutlinedBorder] = field(default=None)
    unselected_label_text_style: Optional[TextStyle] = field(default=None)
    selected_label_text_style: Optional[TextStyle] = field(default=None)
    label_type: Optional[NavigationRailLabelType] = field(default=None)
    min_width: OptionalNumber = field(default=None)
    min_extended_width: OptionalNumber = field(default=None)
    group_alignment: OptionalNumber = field(default=None)
    use_indicator: Optional = field(default=None)


@dataclasses.dataclass
class AppBarTheme:
    color: Optional[str] = field(default=None)
    bgcolor: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    foreground_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    title_text_style: Optional[TextStyle] = field(default=None)
    toolbar_text_style: Optional[TextStyle] = field(default=None)
    center_title: Optional[bool] = field(default=None)
    title_spacing: OptionalNumber = field(default=None)
    scroll_elevation: OptionalNumber = field(default=None)
    toolbar_height: OptionalNumber = field(default=None)


@dataclasses.dataclass
class BottomAppBarTheme:
    color: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    height: OptionalNumber = field(default=None)
    padding: PaddingValue = field(default=None)


@dataclasses.dataclass
class RadioTheme:
    fill_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    splash_radius: OptionalNumber = field(default=None)
    height: OptionalNumber = field(default=None)
    visual_density: Optional[ThemeVisualDensity] = field(default=None)
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, MaterialState], MouseCursor]
    ] = field(default=None)


@dataclasses.dataclass
class CheckboxTheme:
    overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    check_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    fill_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    splash_radius: OptionalNumber = field(default=None)
    border_side: Optional[BorderSide] = field(default=None)
    visual_density: Optional[ThemeVisualDensity] = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, MaterialState], MouseCursor]
    ] = field(default=None)


@dataclasses.dataclass
class BadgeTheme:
    bgcolor: Optional[str] = field(default=None)
    text_color: Optional[str] = field(default=None)
    small_size: OptionalNumber = field(default=None)
    large_size: OptionalNumber = field(default=None)
    alignment: Optional[Alignment] = field(default=None)
    padding: PaddingValue = field(default=None)
    offset: OffsetValue = field(default=None)
    text_style: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class SwitchTheme:
    thumb_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    track_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    track_outline_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    thumb_icon: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    track_outline_width: Union[
        None, Union[int, float], Dict[Union[str, MaterialState], Union[int, float]]
    ] = field(default=None)
    splash_radius: OptionalNumber = field(default=None)
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, MaterialState], MouseCursor]
    ] = field(default=None)


@dataclasses.dataclass
class DividerTheme:
    color: Optional[str] = field(default=None)
    thickness: OptionalNumber = field(default=None)
    space: OptionalNumber = field(default=None)
    leading_indent: OptionalNumber = field(default=None)
    trailing_indent: OptionalNumber = field(default=None)


@dataclasses.dataclass
class SnackBarTheme:
    bgcolor: Optional[str] = field(default=None)
    action_text_color: Optional[str] = field(default=None)
    action_bgcolor: Optional[str] = field(default=None)
    close_icon_color: Optional[str] = field(default=None)
    disabled_action_text_color: Optional[str] = field(default=None)
    disabled_action_bgcolor: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    content_text_style: Optional[TextStyle] = field(default=None)
    width: OptionalNumber = field(default=None)
    alignment: Optional[Alignment] = field(default=None)
    show_close_icon: Optional[bool] = field(default=None)
    dismiss_direction: Optional[DismissDirection] = field(default=None)
    behavior: Optional[SnackBarBehavior] = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    inset_padding: PaddingValue = field(default=None)
    action_overflow_threshold: OptionalNumber = field(default=None)


@dataclasses.dataclass
class BannerTheme:
    bgcolor: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    divider_color: Optional[str] = field(default=None)
    padding: PaddingValue = field(default=None)
    leading_padding: PaddingValue = field(default=None)
    elevation: OptionalNumber = field(default=None)
    content_text_style: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class DatePickerTheme:
    bgcolor: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    divider_color: Optional[str] = field(default=None)
    header_bgcolor: Optional[str] = field(default=None)
    today_bgcolor: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    day_bgcolor: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    day_overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    day_foreground_color: Union[None, str, Dict[Union[str, MaterialState], str]] = (
        field(default=None)
    )
    elevation: OptionalNumber = field(default=None)
    range_picker_elevation: OptionalNumber = field(default=None)
    day_text_style: Optional[TextStyle] = field(default=None)
    weekday_text_style: Optional[TextStyle] = field(default=None)
    year_text_style: Optional[TextStyle] = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    cancel_button_style: Optional[ButtonStyle] = field(default=None)
    confirm_button_style: Optional[ButtonStyle] = field(default=None)
    header_foreground_color: Optional[str] = field(default=None)
    header_headline_text_style: Optional[TextStyle] = field(default=None)
    header_help_text_style: Optional[TextStyle] = field(default=None)
    range_picker_bgcolor: Optional[str] = field(default=None)
    range_picker_header_bgcolor: Optional[str] = field(default=None)
    range_picker_header_foreground_color: Optional[str] = field(default=None)
    today_foreground_color: Union[None, str, Dict[Union[str, MaterialState], str]] = (
        field(default=None)
    )
    range_picker_shape: Optional[OutlinedBorder] = field(default=None)
    range_picker_header_help_text_style: Optional[TextStyle] = field(default=None)
    range_picker_header_headline_text_style: Optional[TextStyle] = field(default=None)
    range_picker_surface_tint_color: Optional[str] = field(default=None)
    range_selection_bgcolor: Optional[str] = field(default=None)
    range_selection_overlay_color: Union[
        None, str, Dict[Union[str, MaterialState], str]
    ] = field(default=None)
    today_border_side: Optional[BorderSide] = field(default=None)
    year_bgcolor: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    year_foreground_color: Union[None, str, Dict[Union[str, MaterialState], str]] = (
        field(default=None)
    )
    year_overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )


@dataclasses.dataclass
class TimePickerTheme:
    bgcolor: Optional[str] = field(default=None)
    day_period_color: Optional[str] = field(default=None)
    day_period_text_color: Optional[str] = field(default=None)
    dial_bgcolor: Optional[str] = field(default=None)
    dial_hand_color: Optional[str] = field(default=None)
    dial_text_color: Optional[str] = field(default=None)
    entry_mode_icon_color: Optional[str] = field(default=None)
    hour_minute_color: Optional[str] = field(default=None)
    hour_minute_text_color: Optional[str] = field(default=None)
    day_period_button_style: Optional[ButtonStyle] = field(default=None)
    cancel_button_style: Optional[ButtonStyle] = field(default=None)
    confirm_button_style: Optional[ButtonStyle] = field(default=None)
    day_period_text_style: Optional[TextStyle] = field(default=None)
    dial_text_style: Optional[TextStyle] = field(default=None)
    help_text_style: Optional[TextStyle] = field(default=None)
    hour_minute_text_style: Optional[TextStyle] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    day_period_shape: Optional[OutlinedBorder] = field(default=None)
    hour_minute_shape: Optional[OutlinedBorder] = field(default=None)
    day_period_border_side: Optional[BorderSide] = field(default=None)
    padding: PaddingValue = field(default=None)


# @dataclasses.dataclass
# class DropdownMenuTheme:
#     menu_style: Optional[MenuStyle] = field(default=None)
#     text_style: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class ListTileTheme:
    icon_color: Optional[str] = field(default=None)
    text_color: Optional[str] = field(default=None)
    bgcolor: Optional[str] = field(default=None)
    selected_tile_color: Optional[str] = field(default=None)
    selected_color: Optional[str] = field(default=None)
    is_three_line: Optional[bool] = field(default=None)
    enable_feedback: Optional[bool] = field(default=None)
    dense: Optional[bool] = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    visual_density: Optional[ThemeVisualDensity] = field(default=None)
    content_padding: PaddingValue = field(default=None)
    min_vertical_padding: PaddingValue = field(default=None)
    horizontal_spacing: OptionalNumber = field(default=None)
    min_leading_width: OptionalNumber = field(default=None)
    title_text_style: Optional[TextStyle] = field(default=None)
    subtitle_text_style: Optional[TextStyle] = field(default=None)
    leading_and_trailing_text_style: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class TooltipTheme:
    height: OptionalNumber = field(default=None)
    text_style: Optional[TextStyle] = field(default=None)
    enable_feedback: Optional[bool] = field(default=None)
    exclude_from_semantics: Optional[bool] = field(default=None)


@dataclasses.dataclass
class ExpansionTileTheme:
    bgcolor: Optional[str] = field(default=None)
    icon_color: Optional[str] = field(default=None)
    text_color: Optional[str] = field(default=None)
    collapsed_bgcolor: Optional[str] = field(default=None)
    collapsed_icon_color: Optional[str] = field(default=None)


@dataclasses.dataclass
class SliderTheme:
    active_track_color: Optional[str] = field(default=None)
    inactive_track_color: Optional[str] = field(default=None)
    thumb_color: Optional[str] = field(default=None)
    overlay_color: Optional[str] = field(default=None)
    value_indicator_color: Optional[str] = field(default=None)
    disabled_thumb_color: Optional[str] = field(default=None)
    value_indicator_text_style: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class ProgressIndicatorTheme:
    color: Optional[str] = field(default=None)
    circular_track_color: Optional[str] = field(default=None)
    linear_track_color: Optional[str] = field(default=None)
    refresh_bgcolor: Optional[str] = field(default=None)
    linear_min_height: OptionalNumber = field(default=None)


@dataclasses.dataclass
class PopupMenuTheme:
    color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    icon_color: Optional[str] = field(default=None)
    text_style: Optional[TextStyle] = field(default=None)
    label_text_style: Optional[TextStyle] = field(default=None)
    enable_feedback: Optional[bool] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    icon_size: OptionalNumber = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    menu_position: Optional[PopupMenuPosition] = field(default=None)
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, MaterialState], MouseCursor]
    ] = field(default=None)


@dataclasses.dataclass
class SearchBarTheme:
    bgcolor: Optional[str] = field(default=None)
    text_capitalization: Optional[TextCapitalization] = field(default=None)
    shadow_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    surface_tint_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    elevation: Union[
        None, Union[int, float], Dict[Union[str, MaterialState], Union[int, float]]
    ] = field(default=None)
    text_style: Union[None, TextStyle, Dict[Union[str, MaterialState], TextStyle]] = (
        field(default=None)
    )
    hint_style: Union[None, TextStyle, Dict[Union[str, MaterialState], TextStyle]] = (
        field(default=None)
    )
    shape: Union[
        None, OutlinedBorder, Dict[Union[str, MaterialState], OutlinedBorder]
    ] = field(default=None)
    padding: Union[
        None,
        Union[int, float, Padding],
        Dict[Union[str, MaterialState], Union[int, float, Padding]],
    ] = field(default=None)


@dataclasses.dataclass
class SearchViewTheme:
    bgcolor: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    divider_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    header_hint_text_style: Optional[TextStyle] = field(default=None)
    header_text_style: Optional[TextStyle] = field(default=None)
    shape: Optional[OutlinedBorder] = field(default=None)
    border_side: Optional[BorderSide] = field(default=None)


@dataclasses.dataclass
class BottomNavigationBarTheme:
    bgcolor: Optional[str] = field(default=None)
    selected_item_color: Optional[str] = field(default=None)
    unselected_item_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    enable_feedback: Optional[bool] = field(default=None)
    show_selected_labels: Optional[bool] = field(default=None)
    show_unselected_labels: Optional[bool] = field(default=None)
    selected_label_text_style: Optional[TextStyle] = field(default=None)
    unselected_label_text_style: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class NavigationDrawerTheme:
    bgcolor: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    indicator_color: Optional[str] = field(default=None)
    elevation: OptionalNumber = field(default=None)
    tile_height: OptionalNumber = field(default=None)
    label_text_style: Union[
        None, TextStyle, Dict[Union[str, MaterialState], TextStyle]
    ] = field(default=None)
    indicator_shape: Optional[OutlinedBorder] = field(default=None)


@dataclasses.dataclass
class NavigationBarTheme:
    bgcolor: Optional[str] = field(default=None)
    shadow_color: Optional[str] = field(default=None)
    surface_tint_color: Optional[str] = field(default=None)
    indicator_color: Optional[str] = field(default=None)
    overlay_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    elevation: OptionalNumber = field(default=None)
    height: OptionalNumber = field(default=None)
    label_text_style: Union[
        None, TextStyle, Dict[Union[str, MaterialState], TextStyle]
    ] = field(default=None)
    indicator_shape: Optional[OutlinedBorder] = field(default=None)
    label_behavior: Optional[NavigationBarLabelBehavior] = field(default=None)


@dataclasses.dataclass
class SegmentedButtonTheme:
    # selected_icon: Optional[str] = field(default=None)
    style: Optional[ButtonStyle] = field(default=None)


@dataclasses.dataclass
class IconTheme:
    color: Optional[str] = field(default=None)
    apply_text_scaling: Optional[bool] = field(default=None)
    fill: OptionalNumber = field(default=None)
    opacity: OptionalNumber = field(default=None)
    size: OptionalNumber = field(default=None)
    optical_size: OptionalNumber = field(default=None)
    grade: OptionalNumber = field(default=None)
    weight: OptionalNumber = field(default=None)
    shadows: Optional[List[BoxShadow]] = field(default=None)


@dataclasses.dataclass
class Theme:
    color_scheme_seed: Optional[str] = field(default=None)
    primary_swatch: Optional[str] = field(default=None)
    font_family: Optional[str] = field(default=None)
    use_material3: Optional[bool] = field(default=None)
    appbar_theme: Optional[AppBarTheme] = field(default=None)
    badge_theme: Optional[BadgeTheme] = field(default=None)
    banner_theme: Optional[BannerTheme] = field(default=None)
    bottom_appbar_theme: Optional[BottomAppBarTheme] = field(default=None)
    bottom_navigation_bar_theme: Optional[BottomNavigationBarTheme] = field(
        default=None
    )
    bottom_sheet_theme: Optional[BottomSheetTheme] = field(default=None)
    card_theme: Optional[CardTheme] = field(default=None)
    checkbox_theme: Optional[CheckboxTheme] = field(default=None)
    chip_theme: Optional[ChipTheme] = field(default=None)
    color_scheme: Optional[ColorScheme] = field(default=None)
    date_picker_theme: Optional[DatePickerTheme] = field(default=None)
    dialog_theme: Optional[DialogTheme] = field(default=None)
    divider_theme: Optional[DividerTheme] = field(default=None)
    # dropdown_menu_theme: Optional[DropdownMenuTheme] = field(default=None)
    expansion_tile_theme: Optional[ExpansionTileTheme] = field(default=None)
    list_tile_theme: Optional[ListTileTheme] = field(default=None)
    navigation_bar_theme: Optional[NavigationBarTheme] = field(default=None)
    navigation_drawer_theme: Optional[NavigationDrawerTheme] = field(default=None)
    navigation_rail_theme: Optional[NavigationRailTheme] = field(default=None)
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
    popup_menu_theme: Optional[PopupMenuTheme] = field(default=None)
    primary_color: Optional[str] = field(default=None)
    primary_color_dark: Optional[str] = field(default=None)
    primary_color_light: Optional[str] = field(default=None)
    primary_text_theme: Optional[TextTheme] = field(default=None)
    progress_indicator_theme: Optional[ProgressIndicatorTheme] = field(default=None)
    radio_theme: Optional[RadioTheme] = field(default=None)
    scrollbar_theme: Optional[ScrollbarTheme] = field(default=None)
    search_bar_theme: Optional[SearchBarTheme] = field(default=None)
    # search_view_theme: Optional[SearchViewTheme] = field(default=None)
    segmented_button_theme: Optional[SegmentedButtonTheme] = field(default=None)
    slider_theme: Optional[SliderTheme] = field(default=None)
    snackbar_theme: Optional[SnackBarTheme] = field(default=None)
    switch_theme: Optional[SwitchTheme] = field(default=None)
    system_overlay_style: SystemOverlayStyle = field(default_factory=SystemOverlayStyle)
    tabs_theme: Optional[TabsTheme] = field(default=None)
    text_theme: Optional[TextTheme] = field(default=None)
    time_picker_theme: Optional[TimePickerTheme] = field(default=None)
    tooltip_theme: Optional[TooltipTheme] = field(default=None)
    visual_density: ThemeVisualDensity = field(default=ThemeVisualDensity.STANDARD)
