from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadius
from flet.controls.box import BoxConstraints, BoxDecoration, BoxShadow
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.control_state import (
    ControlState,
    ControlStateValue,
    OptionalControlStateValue,
)
from flet.controls.duration import OptionalDurationValue
from flet.controls.margin import OptionalMarginValue
from flet.controls.material.menu_bar import MenuStyle
from flet.controls.material.navigation_bar import NavigationBarLabelBehavior
from flet.controls.material.navigation_rail import NavigationRailLabelType
from flet.controls.material.popup_menu_button import PopupMenuPosition
from flet.controls.material.slider import SliderInteraction
from flet.controls.material.snack_bar import DismissDirection, SnackBarBehavior
from flet.controls.material.textfield import TextCapitalization
from flet.controls.material.tooltip import TooltipTriggerMode
from flet.controls.padding import OptionalPaddingValue, PaddingValue
from flet.controls.size import Size
from flet.controls.text_style import TextStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    Brightness,
    ClipBehavior,
    ColorValue,
    IconValue,
    Locale,
    MainAxisAlignment,
    MouseCursor,
    NotchShape,
    OptionalColorValue,
    OptionalNumber,
    StrokeCap,
    TextAlign,
    VisualDensity,
)


class PageTransitionTheme(Enum):
    NONE = "none"
    FADE_UPWARDS = "fadeUpwards"
    OPEN_UPWARDS = "openUpwards"
    ZOOM = "zoom"
    CUPERTINO = "cupertino"
    PREDICTIVE = "predictive"
    FADE_FORWARDS = "fadeForwards"


@dataclass
class PageTransitionsTheme:
    android: Optional[PageTransitionTheme] = None
    ios: Optional[PageTransitionTheme] = None
    linux: Optional[PageTransitionTheme] = None
    macos: Optional[PageTransitionTheme] = None
    windows: Optional[PageTransitionTheme] = None


@dataclass
class ColorScheme:
    primary: OptionalColorValue = None
    on_primary: OptionalColorValue = None
    primary_container: OptionalColorValue = None
    on_primary_container: OptionalColorValue = None
    secondary: OptionalColorValue = None
    on_secondary: OptionalColorValue = None
    secondary_container: OptionalColorValue = None
    on_secondary_container: OptionalColorValue = None
    tertiary: OptionalColorValue = None
    on_tertiary: OptionalColorValue = None
    tertiary_container: OptionalColorValue = None
    on_tertiary_container: OptionalColorValue = None
    error: OptionalColorValue = None
    on_error: OptionalColorValue = None
    error_container: OptionalColorValue = None
    on_error_container: OptionalColorValue = None
    background: OptionalColorValue = None
    on_background: OptionalColorValue = None
    surface: OptionalColorValue = None
    on_surface: OptionalColorValue = None
    surface_variant: OptionalColorValue = None
    on_surface_variant: OptionalColorValue = None
    outline: OptionalColorValue = None
    outline_variant: OptionalColorValue = None
    shadow: OptionalColorValue = None
    scrim: OptionalColorValue = None
    inverse_surface: OptionalColorValue = None
    on_inverse_surface: OptionalColorValue = None
    inverse_primary: OptionalColorValue = None
    surface_tint: OptionalColorValue = None
    on_primary_fixed: OptionalColorValue = None
    on_secondary_fixed: OptionalColorValue = None
    on_tertiary_fixed: OptionalColorValue = None
    on_primary_fixed_variant: OptionalColorValue = None
    on_secondary_fixed_variant: OptionalColorValue = None
    on_tertiary_fixed_variant: OptionalColorValue = None
    primary_fixed: OptionalColorValue = None
    secondary_fixed: OptionalColorValue = None
    tertiary_fixed: OptionalColorValue = None
    primary_fixed_dim: OptionalColorValue = None
    secondary_fixed_dim: OptionalColorValue = None
    surface_bright: OptionalColorValue = None
    surface_container: OptionalColorValue = None
    surface_container_high: OptionalColorValue = None
    surface_container_low: OptionalColorValue = None
    surface_container_lowest: OptionalColorValue = None
    surface_dim: OptionalColorValue = None
    tertiary_fixed_dim: OptionalColorValue = None


@dataclass
class TextTheme:
    body_large: Optional[TextStyle] = None
    body_medium: Optional[TextStyle] = None
    body_small: Optional[TextStyle] = None
    display_large: Optional[TextStyle] = None
    display_medium: Optional[TextStyle] = None
    display_small: Optional[TextStyle] = None
    headline_large: Optional[TextStyle] = None
    headline_medium: Optional[TextStyle] = None
    headline_small: Optional[TextStyle] = None
    label_large: Optional[TextStyle] = None
    label_medium: Optional[TextStyle] = None
    label_small: Optional[TextStyle] = None
    title_large: Optional[TextStyle] = None
    title_medium: Optional[TextStyle] = None
    title_small: Optional[TextStyle] = None


@dataclass
class ScrollbarTheme:
    thumb_visibility: OptionalControlStateValue[bool] = None
    thickness: OptionalControlStateValue[OptionalNumber] = None
    track_visibility: OptionalControlStateValue[bool] = None
    radius: Optional[float] = None
    thumb_color: OptionalControlStateValue[ColorValue] = None
    track_color: OptionalControlStateValue[ColorValue] = None
    track_border_color: OptionalControlStateValue[ColorValue] = None
    cross_axis_margin: Optional[float] = None
    main_axis_margin: Optional[float] = None
    min_thumb_length: Optional[float] = None
    interactive: Optional[bool] = None

    def __post_init__(self):
        if not isinstance(self.thumb_visibility, dict):
            self.thumb_visibility = {ControlState.DEFAULT: self.thumb_visibility}
        if not isinstance(self.thickness, dict):
            self.thickness = {ControlState.DEFAULT: self.thickness}
        if not isinstance(self.track_visibility, dict):
            self.track_visibility = {ControlState.DEFAULT: self.track_visibility}
        if not isinstance(self.thumb_color, dict):
            self.thumb_color = {ControlState.DEFAULT: self.thumb_color}
        if not isinstance(self.track_color, dict):
            self.track_color = {ControlState.DEFAULT: self.track_color}
        if not isinstance(self.track_border_color, dict):
            self.track_border_color = {ControlState.DEFAULT: self.track_border_color}


@dataclass
class TabsTheme:
    divider_color: OptionalColorValue = None
    indicator_border_radius: Optional[BorderRadius] = None
    indicator_border_side: Optional[BorderSide] = None
    indicator_padding: OptionalPaddingValue = None
    indicator_color: OptionalColorValue = None
    indicator_tab_size: Optional[bool] = None
    label_color: OptionalColorValue = None
    unselected_label_color: OptionalColorValue = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    label_padding: OptionalPaddingValue = None
    label_text_style: Optional[TextStyle] = None
    unselected_label_text_style: Optional[TextStyle] = None

    def __post_init__(self):
        if not isinstance(self.overlay_color, dict):
            self.overlay_color = {ControlState.DEFAULT: self.overlay_color}
        if not isinstance(self.mouse_cursor, dict):
            self.mouse_cursor = {ControlState.DEFAULT: self.mouse_cursor}


@dataclass
class SystemOverlayStyle:
    status_bar_color: OptionalColorValue = None
    system_navigation_bar_color: OptionalColorValue = None
    system_navigation_bar_divider_color: OptionalColorValue = None
    enforce_system_navigation_bar_contrast: Optional[bool] = None
    enforce_system_status_bar_contrast: Optional[bool] = None
    system_navigation_bar_icon_brightness: Optional[Brightness] = None
    status_bar_brightness: Optional[Brightness] = None
    status_bar_icon_brightness: Optional[Brightness] = None


@dataclass
class DialogTheme:
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    title_text_style: Optional[TextStyle] = None
    content_text_style: Optional[TextStyle] = None
    alignment: Optional[Alignment] = None
    actions_padding: OptionalPaddingValue = None
    clip_behavior: Optional[ClipBehavior] = None
    barrier_color: OptionalColorValue = None
    inset_padding: OptionalPaddingValue = None


@dataclass
class ElevatedButtonTheme:
    bgcolor: OptionalColorValue = None
    foreground_color: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    disabled_bgcolor: OptionalColorValue = None
    disabled_foreground_color: OptionalColorValue = None
    disabled_icon_color: OptionalColorValue = None
    overlay_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    padding: OptionalPaddingValue = None
    enable_feedback: Optional[bool] = None
    disabled_mouse_cursor: Optional[MouseCursor] = None
    enabled_mouse_cursor: Optional[MouseCursor] = None
    shape: Optional[OutlinedBorder] = None
    text_style: Optional[TextStyle] = None
    visual_density: Optional[VisualDensity] = None
    border_side: Optional[BorderSide] = None
    animation_duration: OptionalDurationValue = None
    alignment: Optional[Alignment] = None
    icon_size: OptionalNumber = None
    fixed_size: Optional[Size] = None
    maximum_size: Optional[Size] = None
    minimum_size: Optional[Size] = None


@dataclass
class OutlinedButtonTheme(ElevatedButtonTheme):
    pass


@dataclass
class TextButtonTheme(ElevatedButtonTheme):
    pass


@dataclass
class FilledButtonTheme(ElevatedButtonTheme):
    pass


@dataclass
class IconButtonTheme:
    # from ElevatedButtonTheme (excluding icon_color, disabled_icon_color, text_style)
    bgcolor: OptionalColorValue = None
    foreground_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    disabled_bgcolor: OptionalColorValue = None
    disabled_foreground_color: OptionalColorValue = None
    overlay_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    padding: OptionalPaddingValue = None
    enable_feedback: Optional[bool] = None
    disabled_mouse_cursor: Optional[MouseCursor] = None
    enabled_mouse_cursor: Optional[MouseCursor] = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Optional[VisualDensity] = None
    border_side: Optional[BorderSide] = None
    animation_duration: OptionalDurationValue = None
    alignment: Optional[Alignment] = None
    icon_size: OptionalNumber = None
    fixed_size: Optional[Size] = None
    maximum_size: Optional[Size] = None
    minimum_size: Optional[Size] = None
    # Icon Button Theme
    focus_color: OptionalColorValue = None
    highlight_color: OptionalColorValue = None
    hover_color: OptionalColorValue = None


@dataclass
class BottomSheetTheme:
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    drag_handle_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    show_drag_handle: Optional[bool] = None
    modal_bgcolor: OptionalColorValue = None
    modal_elevation: OptionalNumber = None
    clip_behavior: Optional[ClipBehavior] = None
    size_constraints: Optional[BoxConstraints] = None
    modal_barrier_color: OptionalColorValue = None


@dataclass
class CardTheme:
    color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    clip_behavior: Optional[ClipBehavior] = None
    margin: OptionalMarginValue = None


@dataclass
class ChipTheme:
    color: OptionalControlStateValue[ColorValue] = None
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    disabled_color: OptionalColorValue = None
    selected_color: OptionalColorValue = None
    checkmark_color: OptionalColorValue = None
    delete_icon_color: OptionalColorValue = None
    secondary_selected_color: OptionalColorValue = None
    selected_shadow_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    click_elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    padding: OptionalPaddingValue = None
    label_padding: OptionalPaddingValue = None
    label_text_style: Optional[TextStyle] = None
    secondary_label_text_style: Optional[TextStyle] = None
    border_side: Optional[BorderSide] = None
    brightness: Optional[Brightness] = None
    show_checkmark: Optional[bool] = None
    avatar_constraints: Optional[BoxConstraints] = None
    delete_icon_size_constraints: Optional[BoxConstraints] = None

    def __post_init__(self):
        if not isinstance(self.color, dict):
            self.color = {ControlState.DEFAULT: self.color}


@dataclass
class FloatingActionButtonTheme:
    bgcolor: OptionalColorValue = None
    hover_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    foreground_color: OptionalColorValue = None
    splash_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    focus_elevation: OptionalNumber = None
    hover_elevation: OptionalNumber = None
    highlight_elevation: OptionalNumber = None
    disabled_elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    enable_feedback: Optional[bool] = None
    extended_padding: OptionalPaddingValue = None
    extended_text_style: Optional[TextStyle] = None
    extended_icon_label_spacing: OptionalNumber = None
    extended_size_constraints: Optional[BoxConstraints] = None
    size_constraints: Optional[BoxConstraints] = None
    large_size_constraints: Optional[BoxConstraints] = None
    small_size_constraints: Optional[BoxConstraints] = None


@dataclass
class NavigationRailTheme:
    bgcolor: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    indicator_shape: Optional[OutlinedBorder] = None
    unselected_label_text_style: Optional[TextStyle] = None
    selected_label_text_style: Optional[TextStyle] = None
    label_type: Optional[NavigationRailLabelType] = None
    min_width: OptionalNumber = None
    min_extended_width: OptionalNumber = None
    group_alignment: OptionalNumber = None
    use_indicator: Optional[bool] = None


@dataclass
class AppBarTheme:
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    foreground_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    title_text_style: Optional[TextStyle] = None
    toolbar_text_style: Optional[TextStyle] = None
    center_title: Optional[bool] = None
    title_spacing: OptionalNumber = None
    scroll_elevation: OptionalNumber = None
    toolbar_height: OptionalNumber = None
    actions_padding: OptionalPaddingValue = None


@dataclass
class BottomAppBarTheme:
    color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    height: OptionalNumber = None
    padding: OptionalPaddingValue = None
    shape: Optional[NotchShape] = None


@dataclass
class RadioTheme:
    fill_color: OptionalControlStateValue[ColorValue] = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    splash_radius: OptionalNumber = None
    height: OptionalNumber = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None

    def __post_init__(self):
        if not isinstance(self.fill_color, dict):
            self.fill_color = {ControlState.DEFAULT: self.fill_color}
        if not isinstance(self.overlay_color, dict):
            self.overlay_color = {ControlState.DEFAULT: self.overlay_color}
        if not isinstance(self.mouse_cursor, dict):
            self.mouse_cursor = {ControlState.DEFAULT: self.mouse_cursor}


@dataclass
class CheckboxTheme:
    overlay_color: OptionalControlStateValue[ColorValue] = None
    check_color: OptionalControlStateValue[ColorValue] = None
    fill_color: OptionalControlStateValue[ColorValue] = None
    splash_radius: OptionalNumber = None
    border_side: Optional[BorderSide] = None
    visual_density: Optional[VisualDensity] = None
    shape: Optional[OutlinedBorder] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None

    def __post_init__(self):
        if not isinstance(self.overlay_color, dict):
            self.overlay_color = {ControlState.DEFAULT: self.overlay_color}
        if not isinstance(self.check_color, dict):
            self.check_color = {ControlState.DEFAULT: self.check_color}
        if not isinstance(self.fill_color, dict):
            self.fill_color = {ControlState.DEFAULT: self.fill_color}
        if not isinstance(self.mouse_cursor, dict):
            self.mouse_cursor = {ControlState.DEFAULT: self.mouse_cursor}


@dataclass
class BadgeTheme:
    bgcolor: OptionalColorValue = None
    text_color: OptionalColorValue = None
    small_size: OptionalNumber = None
    large_size: OptionalNumber = None
    alignment: Optional[Alignment] = None
    padding: OptionalPaddingValue = None
    offset: Optional[OffsetValue] = None
    text_style: Optional[TextStyle] = None


@dataclass
class SwitchTheme:
    thumb_color: OptionalControlStateValue[ColorValue] = None
    track_color: OptionalControlStateValue[ColorValue] = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    track_outline_color: OptionalControlStateValue[ColorValue] = None
    thumb_icon: OptionalControlStateValue[str] = None
    track_outline_width: OptionalControlStateValue[OptionalNumber] = None
    splash_radius: OptionalNumber = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    padding: OptionalPaddingValue = None

    def __post_init__(self):
        if not isinstance(self.thumb_color, dict):
            self.thumb_color = {ControlState.DEFAULT: self.thumb_color}
        if not isinstance(self.track_color, dict):
            self.track_color = {ControlState.DEFAULT: self.track_color}
        if not isinstance(self.overlay_color, dict):
            self.overlay_color = {ControlState.DEFAULT: self.overlay_color}
        if not isinstance(self.track_outline_color, dict):
            self.track_outline_color = {ControlState.DEFAULT: self.track_outline_color}
        if not isinstance(self.thumb_icon, dict):
            self.thumb_icon = {ControlState.DEFAULT: self.thumb_icon}
        if not isinstance(self.track_outline_width, dict):
            self.track_outline_width = {ControlState.DEFAULT: self.track_outline_width}
        if not isinstance(self.mouse_cursor, dict):
            self.mouse_cursor = {ControlState.DEFAULT: self.mouse_cursor}


@dataclass
class DividerTheme:
    color: OptionalColorValue = None
    thickness: OptionalNumber = None
    space: OptionalNumber = None
    leading_indent: OptionalNumber = None
    trailing_indent: OptionalNumber = None


@dataclass
class SnackBarTheme:
    bgcolor: OptionalColorValue = None
    action_text_color: OptionalColorValue = None
    action_bgcolor: OptionalColorValue = None
    close_icon_color: OptionalColorValue = None
    disabled_action_text_color: OptionalColorValue = None
    disabled_action_bgcolor: OptionalColorValue = None
    elevation: OptionalNumber = None
    content_text_style: Optional[TextStyle] = None
    width: OptionalNumber = None
    alignment: Optional[Alignment] = None
    show_close_icon: Optional[bool] = None
    dismiss_direction: Optional[DismissDirection] = None
    behavior: Optional[SnackBarBehavior] = None
    shape: Optional[OutlinedBorder] = None
    inset_padding: OptionalPaddingValue = None
    action_overflow_threshold: OptionalNumber = None


@dataclass
class BannerTheme:
    bgcolor: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    divider_color: OptionalColorValue = None
    padding: OptionalPaddingValue = None
    leading_padding: OptionalPaddingValue = None
    elevation: OptionalNumber = None
    content_text_style: Optional[TextStyle] = None


@dataclass
class DatePickerTheme:
    bgcolor: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    divider_color: OptionalColorValue = None
    header_bgcolor: OptionalColorValue = None
    today_bgcolor: OptionalControlStateValue[ColorValue] = None
    day_bgcolor: OptionalControlStateValue[ColorValue] = None
    day_overlay_color: OptionalControlStateValue[ColorValue] = None
    day_foreground_color: OptionalControlStateValue[ColorValue] = None
    elevation: OptionalNumber = None
    range_picker_elevation: OptionalNumber = None
    day_text_style: Optional[TextStyle] = None
    weekday_text_style: Optional[TextStyle] = None
    year_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None
    cancel_button_style: Optional[ButtonStyle] = None
    confirm_button_style: Optional[ButtonStyle] = None
    header_foreground_color: OptionalColorValue = None
    header_headline_text_style: Optional[TextStyle] = None
    header_help_text_style: Optional[TextStyle] = None
    range_picker_bgcolor: OptionalColorValue = None
    range_picker_header_bgcolor: OptionalColorValue = None
    range_picker_header_foreground_color: OptionalColorValue = None
    today_foreground_color: OptionalControlStateValue[ColorValue] = None
    range_picker_shape: Optional[OutlinedBorder] = None
    range_picker_header_help_text_style: Optional[TextStyle] = None
    range_picker_header_headline_text_style: Optional[TextStyle] = None
    range_picker_surface_tint_color: OptionalColorValue = None
    range_selection_bgcolor: OptionalColorValue = None
    range_selection_overlay_color: OptionalControlStateValue[ColorValue] = None
    today_border_side: Optional[BorderSide] = None
    year_bgcolor: OptionalControlStateValue[ColorValue] = None
    year_foreground_color: OptionalControlStateValue[ColorValue] = None
    year_overlay_color: OptionalControlStateValue[ColorValue] = None
    day_shape: OptionalControlStateValue[OutlinedBorder] = None
    locale: Optional[Locale] = None

    def __post_init__(self):
        if not isinstance(self.today_bgcolor, dict):
            self.today_bgcolor = {ControlState.DEFAULT: self.today_bgcolor}
        if not isinstance(self.day_bgcolor, dict):
            self.day_bgcolor = {ControlState.DEFAULT: self.day_bgcolor}
        if not isinstance(self.day_overlay_color, dict):
            self.day_overlay_color = {ControlState.DEFAULT: self.day_overlay_color}
        if not isinstance(self.day_foreground_color, dict):
            self.day_foreground_color = {
                ControlState.DEFAULT: self.day_foreground_color
            }
        if not isinstance(self.today_foreground_color, dict):
            self.today_foreground_color = {
                ControlState.DEFAULT: self.today_foreground_color
            }
        if not isinstance(self.range_selection_overlay_color, dict):
            self.range_selection_overlay_color = {
                ControlState.DEFAULT: self.range_selection_overlay_color
            }
        if not isinstance(self.year_bgcolor, dict):
            self.year_bgcolor = {ControlState.DEFAULT: self.year_bgcolor}
        if not isinstance(self.year_foreground_color, dict):
            self.year_foreground_color = {
                ControlState.DEFAULT: self.year_foreground_color
            }
        if not isinstance(self.year_overlay_color, dict):
            self.year_overlay_color = {ControlState.DEFAULT: self.year_overlay_color}
        if not isinstance(self.day_shape, dict):
            self.day_shape = {ControlState.DEFAULT: self.day_shape}


@dataclass
class TimePickerTheme:
    bgcolor: OptionalColorValue = None
    day_period_color: OptionalColorValue = None
    day_period_text_color: OptionalColorValue = None
    dial_bgcolor: OptionalColorValue = None
    dial_hand_color: OptionalColorValue = None
    dial_text_color: OptionalColorValue = None
    entry_mode_icon_color: OptionalColorValue = None
    hour_minute_color: OptionalColorValue = None
    hour_minute_text_color: OptionalColorValue = None
    day_period_button_style: Optional[ButtonStyle] = None
    cancel_button_style: Optional[ButtonStyle] = None
    confirm_button_style: Optional[ButtonStyle] = None
    day_period_text_style: Optional[TextStyle] = None
    dial_text_style: Optional[TextStyle] = None
    help_text_style: Optional[TextStyle] = None
    hour_minute_text_style: Optional[TextStyle] = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    day_period_shape: Optional[OutlinedBorder] = None
    hour_minute_shape: Optional[OutlinedBorder] = None
    day_period_border_side: Optional[BorderSide] = None
    padding: OptionalPaddingValue = None
    time_selector_separator_color: OptionalControlStateValue[ColorValue] = None
    time_selector_separator_text_style: OptionalControlStateValue[TextStyle] = None

    def __post_init__(self):
        if not isinstance(self.time_selector_separator_color, dict):
            self.time_selector_separator_color = {
                ControlState.DEFAULT: self.time_selector_separator_color
            }
        if not isinstance(self.time_selector_separator_text_style, dict):
            self.time_selector_separator_text_style = {
                ControlState.DEFAULT: self.time_selector_separator_text_style
            }


@dataclass
class DropdownMenuTheme:
    menu_style: Optional[MenuStyle] = None
    text_style: Optional[TextStyle] = None


@dataclass
class ListTileTheme:
    icon_color: OptionalColorValue = None
    text_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    selected_tile_color: OptionalColorValue = None
    selected_color: OptionalColorValue = None
    is_three_line: Optional[bool] = None
    enable_feedback: Optional[bool] = None
    dense: Optional[bool] = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Optional[VisualDensity] = None
    content_padding: OptionalPaddingValue = None
    min_vertical_padding: OptionalPaddingValue = None
    horizontal_spacing: OptionalNumber = None
    min_leading_width: OptionalNumber = None
    title_text_style: Optional[TextStyle] = None
    subtitle_text_style: Optional[TextStyle] = None
    leading_and_trailing_text_style: Optional[TextStyle] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    min_tile_height: OptionalNumber = None

    def __post_init__(self):
        if not isinstance(self.mouse_cursor, dict):
            self.mouse_cursor = {ControlState.DEFAULT: self.mouse_cursor}


@dataclass
class TooltipTheme:
    height: OptionalNumber = None
    text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    exclude_from_semantics: Optional[bool] = None
    prefer_below: Optional[bool] = None
    vertical_offset: OptionalNumber = None
    padding: OptionalPaddingValue = None
    wait_duration: OptionalDurationValue = None
    exit_duration: OptionalDurationValue = None
    show_duration: OptionalDurationValue = None
    margin: OptionalMarginValue = None
    trigger_mode: Optional[TooltipTriggerMode] = None
    decoration: Optional[BoxDecoration] = None
    text_align: Optional[TextAlign] = None


@dataclass
class ExpansionTileTheme:
    bgcolor: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    text_color: OptionalColorValue = None
    collapsed_bgcolor: OptionalColorValue = None
    collapsed_icon_color: OptionalColorValue = None
    clip_behavior: Optional[ClipBehavior] = None
    collapsed_text_color: OptionalColorValue = None
    tile_padding: OptionalPaddingValue = None
    expanded_alignment: Optional[Alignment] = None
    controls_padding: OptionalPaddingValue = None


@dataclass
class SliderTheme:
    active_track_color: OptionalColorValue = None
    inactive_track_color: OptionalColorValue = None
    thumb_color: OptionalColorValue = None
    overlay_color: OptionalColorValue = None
    value_indicator_color: OptionalColorValue = None
    disabled_thumb_color: OptionalColorValue = None
    value_indicator_text_style: Optional[TextStyle] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    active_tick_mark_color: OptionalColorValue = None
    disabled_active_tick_mark_color: OptionalColorValue = None
    disabled_active_track_color: OptionalColorValue = None
    disabled_inactive_tick_mark_color: OptionalColorValue = None
    disabled_inactive_track_color: OptionalColorValue = None
    disabled_secondary_active_track_color: OptionalColorValue = None
    inactive_tick_mark_color: OptionalColorValue = None
    overlapping_shape_stroke_color: OptionalColorValue = None
    min_thumb_separation: OptionalNumber = None
    secondary_active_track_color: OptionalColorValue = None
    track_height: OptionalNumber = None
    value_indicator_stroke_color: OptionalColorValue = None
    interaction: Optional[SliderInteraction] = None
    padding: OptionalPaddingValue = None
    track_gap: OptionalNumber = None
    thumb_size: OptionalControlStateValue[Size] = None
    year_2023: Optional[bool] = None

    def __post_init__(self):
        if not isinstance(self.mouse_cursor, dict):
            self.mouse_cursor = {ControlState.DEFAULT: self.mouse_cursor}
        if not isinstance(self.thumb_size, dict):
            self.thumb_size = {ControlState.DEFAULT: self.thumb_size}


@dataclass
class ProgressIndicatorTheme:
    color: OptionalColorValue = None
    circular_track_color: OptionalColorValue = None
    linear_track_color: OptionalColorValue = None
    refresh_bgcolor: OptionalColorValue = None
    linear_min_height: OptionalNumber = None
    border_radius: Optional[BorderRadius] = None
    track_gap: OptionalNumber = None
    circular_track_padding: OptionalPaddingValue = None
    size_constraints: Optional[BoxConstraints] = None
    stop_indicator_color: OptionalColorValue = None
    stop_indicator_radius: OptionalNumber = None
    stroke_align: OptionalNumber = None
    stroke_cap: Optional[StrokeCap] = None
    stroke_width: OptionalNumber = None
    year_2023: Optional[bool] = None


@dataclass
class PopupMenuTheme:
    color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    text_style: Optional[TextStyle] = None
    label_text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    elevation: OptionalNumber = None
    icon_size: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    menu_position: Optional[PopupMenuPosition] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    menu_padding: OptionalPaddingValue = None


@dataclass
class SearchBarTheme:
    bgcolor: OptionalColorValue = None
    text_capitalization: Optional[TextCapitalization] = None
    shadow_color: OptionalControlStateValue[ColorValue] = None
    surface_tint_color: OptionalControlStateValue[ColorValue] = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    elevation: ControlStateValue[OptionalNumber] = None
    text_style: ControlStateValue[TextStyle] = None
    hint_style: ControlStateValue[TextStyle] = None
    shape: ControlStateValue[OutlinedBorder] = None
    padding: ControlStateValue[PaddingValue] = None
    size_constraints: Optional[BoxConstraints] = None
    border_side: ControlStateValue[BorderSide] = None

    def __post_init__(self):
        if not isinstance(self.shadow_color, dict):
            self.shadow_color = {ControlState.DEFAULT: self.shadow_color}
        if not isinstance(self.surface_tint_color, dict):
            self.surface_tint_color = {ControlState.DEFAULT: self.surface_tint_color}
        if not isinstance(self.overlay_color, dict):
            self.overlay_color = {ControlState.DEFAULT: self.overlay_color}
        if not isinstance(self.elevation, dict):
            self.elevation = {ControlState.DEFAULT: self.elevation}
        if not isinstance(self.text_style, dict):
            self.text_style = {ControlState.DEFAULT: self.text_style}
        if not isinstance(self.hint_style, dict):
            self.hint_style = {ControlState.DEFAULT: self.hint_style}
        if not isinstance(self.shape, dict):
            self.shape = {ControlState.DEFAULT: self.shape}
        if not isinstance(self.padding, dict):
            self.padding = {ControlState.DEFAULT: self.padding}
        if not isinstance(self.border_side, dict):
            self.border_side = {ControlState.DEFAULT: self.border_side}


@dataclass
class SearchViewTheme:
    bgcolor: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    divider_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    header_hint_text_style: Optional[TextStyle] = None
    header_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None
    border_side: Optional[BorderSide] = None
    size_constraints: Optional[BoxConstraints] = None
    header_height: OptionalNumber = None
    padding: OptionalPaddingValue = None
    bar_padding: OptionalPaddingValue = None
    shrink_wrap: Optional[bool] = None


@dataclass
class NavigationDrawerTheme:
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    tile_height: OptionalNumber = None
    label_text_style: ControlStateValue[TextStyle] = None
    indicator_shape: Optional[OutlinedBorder] = None
    indicator_size: Optional[Size] = None

    def __post_init__(self):
        if not isinstance(self.label_text_style, dict):
            self.label_text_style = {ControlState.DEFAULT: self.label_text_style}


@dataclass
class NavigationBarTheme:
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    overlay_color: ControlStateValue[ColorValue] = None
    elevation: OptionalNumber = None
    height: OptionalNumber = None
    label_text_style: ControlStateValue[TextStyle] = None
    indicator_shape: Optional[OutlinedBorder] = None
    label_behavior: Optional[NavigationBarLabelBehavior] = None
    label_padding: OptionalPaddingValue = None

    def __post_init__(self):
        if not isinstance(self.label_text_style, dict):
            self.label_text_style = {ControlState.DEFAULT: self.label_text_style}
        if not isinstance(self.overlay_color, dict):
            self.overlay_color = {ControlState.DEFAULT: self.overlay_color}


@dataclass
class SegmentedButtonTheme:
    selected_icon: Optional[IconValue] = None
    style: Optional[ButtonStyle] = None


@dataclass
class IconTheme:
    color: OptionalColorValue = None
    apply_text_scaling: Optional[bool] = None
    fill: OptionalNumber = None
    opacity: OptionalNumber = None
    size: OptionalNumber = None
    optical_size: OptionalNumber = None
    grade: OptionalNumber = None
    weight: OptionalNumber = None
    shadows: Optional[List[BoxShadow]] = None


@dataclass
class DataTableTheme:
    checkbox_horizontal_margin: OptionalNumber = None
    column_spacing: OptionalNumber = None
    data_row_max_height: OptionalNumber = None
    data_row_min_height: OptionalNumber = None
    data_row_color: ControlStateValue[ColorValue] = None
    data_text_style: Optional[TextStyle] = None
    divider_thickness: OptionalNumber = None
    horizontal_margin: OptionalNumber = None
    heading_text_style: Optional[TextStyle] = None
    heading_row_color: ControlStateValue[ColorValue] = None
    heading_row_height: OptionalNumber = None
    data_row_cursor: ControlStateValue[MouseCursor] = None
    decoration: Optional[BoxDecoration] = None
    heading_row_alignment: Optional[MainAxisAlignment] = None
    heading_cell_cursor: ControlStateValue[MouseCursor] = None


@dataclass
class Theme:
    color_scheme_seed: OptionalColorValue = None
    primary_swatch: OptionalColorValue = None
    font_family: Optional[str] = None
    use_material3: Optional[bool] = None
    appbar_theme: Optional[AppBarTheme] = None
    badge_theme: Optional[BadgeTheme] = None
    banner_theme: Optional[BannerTheme] = None
    bottom_appbar_theme: Optional[BottomAppBarTheme] = None
    bottom_sheet_theme: Optional[BottomSheetTheme] = None
    card_theme: Optional[CardTheme] = None
    checkbox_theme: Optional[CheckboxTheme] = None
    chip_theme: Optional[ChipTheme] = None
    color_scheme: Optional[ColorScheme] = None
    data_table_theme: Optional[DataTableTheme] = None
    date_picker_theme: Optional[DatePickerTheme] = None
    dialog_theme: Optional[DialogTheme] = None
    divider_theme: Optional[DividerTheme] = None
    # dropdown_menu_theme: Optional[DropdownMenuTheme] = None
    elevated_button_theme: Optional[ElevatedButtonTheme] = None
    outlined_button_theme: Optional[OutlinedButtonTheme] = None
    text_button_theme: Optional[TextButtonTheme] = None
    filled_button_theme: Optional[FilledButtonTheme] = None
    icon_button_theme: Optional[IconButtonTheme] = None
    expansion_tile_theme: Optional[ExpansionTileTheme] = None
    floating_action_button_theme: Optional[FloatingActionButtonTheme] = None
    icon_theme: Optional[IconTheme] = None
    list_tile_theme: Optional[ListTileTheme] = None
    navigation_bar_theme: Optional[NavigationBarTheme] = None
    navigation_drawer_theme: Optional[NavigationDrawerTheme] = None
    navigation_rail_theme: Optional[NavigationRailTheme] = None
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
    popup_menu_theme: Optional[PopupMenuTheme] = None
    splash_color: OptionalColorValue = None
    highlight_color: OptionalColorValue = None
    hover_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    unselected_control_color: OptionalColorValue = None
    disabled_color: OptionalColorValue = None
    canvas_color: OptionalColorValue = None
    scaffold_bgcolor: OptionalColorValue = None
    card_color: OptionalColorValue = None
    divider_color: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    hint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    secondary_header_color: OptionalColorValue = None
    primary_color: OptionalColorValue = None
    primary_color_dark: OptionalColorValue = None
    primary_color_light: OptionalColorValue = None
    primary_text_theme: Optional[TextTheme] = None
    progress_indicator_theme: Optional[ProgressIndicatorTheme] = None
    radio_theme: Optional[RadioTheme] = None
    scrollbar_theme: Optional[ScrollbarTheme] = None
    search_bar_theme: Optional[SearchBarTheme] = None
    search_view_theme: Optional[SearchViewTheme] = None
    segmented_button_theme: Optional[SegmentedButtonTheme] = None
    slider_theme: Optional[SliderTheme] = None
    snackbar_theme: Optional[SnackBarTheme] = None
    switch_theme: Optional[SwitchTheme] = None
    system_overlay_style: SystemOverlayStyle = field(default_factory=SystemOverlayStyle)
    tabs_theme: Optional[TabsTheme] = None
    text_theme: Optional[TextTheme] = None
    time_picker_theme: Optional[TimePickerTheme] = None
    tooltip_theme: Optional[TooltipTheme] = None
    visual_density: Optional[VisualDensity] = None
