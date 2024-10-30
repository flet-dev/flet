from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union

from flet_core.alignment import Alignment
from flet_core.border import BorderSide
from flet_core.border_radius import BorderRadius
from flet_core.box import BoxDecoration, BoxShadow
from flet_core.buttons import ButtonStyle, OutlinedBorder
from flet_core.control import OptionalNumber
from flet_core.navigation_bar import NavigationBarLabelBehavior
from flet_core.navigation_rail import NavigationRailLabelType
from flet_core.popup_menu_button import PopupMenuPosition
from flet_core.snack_bar import DismissDirection, SnackBarBehavior
from flet_core.text_style import TextStyle
from flet_core.textfield import TextCapitalization
from flet_core.types import (
    Brightness,
    ClipBehavior,
    ColorValue,
    ControlState,
    ControlStateValue,
    MainAxisAlignment,
    MarginValue,
    MouseCursor,
    OffsetValue,
    PaddingValue,
    ThemeVisualDensity,
    VisualDensity,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class PageTransitionTheme(Enum):
    NONE = "none"
    FADE_UPWARDS = "fadeUpwards"
    OPEN_UPWARDS = "openUpwards"
    ZOOM = "zoom"
    CUPERTINO = "cupertino"


@dataclass
class PageTransitionsTheme:
    android: Optional[PageTransitionTheme] = None
    ios: Optional[PageTransitionTheme] = None
    linux: Optional[PageTransitionTheme] = None
    macos: Optional[PageTransitionTheme] = None
    windows: Optional[PageTransitionTheme] = None


@dataclass
class ColorScheme:
    primary: Optional[str] = None
    on_primary: Optional[str] = None
    primary_container: Optional[str] = None
    on_primary_container: Optional[str] = None
    secondary: Optional[str] = None
    on_secondary: Optional[str] = None
    secondary_container: Optional[str] = None
    on_secondary_container: Optional[str] = None
    tertiary: Optional[str] = None
    on_tertiary: Optional[str] = None
    tertiary_container: Optional[str] = None
    on_tertiary_container: Optional[str] = None
    error: Optional[str] = None
    on_error: Optional[str] = None
    error_container: Optional[str] = None
    on_error_container: Optional[str] = None
    background: Optional[str] = None
    on_background: Optional[str] = None
    surface: Optional[str] = None
    on_surface: Optional[str] = None
    surface_variant: Optional[str] = None
    on_surface_variant: Optional[str] = None
    outline: Optional[str] = None
    outline_variant: Optional[str] = None
    shadow: Optional[str] = None
    scrim: Optional[str] = None
    inverse_surface: Optional[str] = None
    on_inverse_surface: Optional[str] = None
    inverse_primary: Optional[str] = None
    surface_tint: Optional[str] = None


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
    thumb_visibility: ControlStateValue[bool] = None
    thickness: ControlStateValue[OptionalNumber] = None
    track_visibility: ControlStateValue[bool] = None
    radius: Optional[float] = None
    thumb_color: ControlStateValue[ColorValue] = None
    track_color: ControlStateValue[ColorValue] = None
    track_border_color: ControlStateValue[ColorValue] = None
    cross_axis_margin: Optional[float] = None
    main_axis_margin: Optional[float] = None
    min_thumb_length: Optional[float] = None
    interactive: Optional[bool] = None


@dataclass
class TabsTheme:
    divider_color: Optional[ColorValue] = None
    indicator_border_radius: Optional[BorderRadius] = None
    indicator_border_side: Optional[BorderSide] = None
    indicator_padding: PaddingValue = None
    indicator_color: Optional[ColorValue] = None
    indicator_tab_size: Optional[bool] = None
    label_color: Optional[ColorValue] = None
    unselected_label_color: Optional[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    mouse_cursor: ControlStateValue[MouseCursor] = None
    label_padding: PaddingValue = None
    label_text_style: Optional[TextStyle] = None
    unselected_label_text_style: Optional[TextStyle] = None


@dataclass
class SystemOverlayStyle:
    status_bar_color: Optional[ColorValue] = None
    system_navigation_bar_color: Optional[ColorValue] = None
    system_navigation_bar_divider_color: Optional[ColorValue] = None
    enforce_system_navigation_bar_contrast: Optional[bool] = None
    enforce_system_status_bar_contrast: Optional[bool] = None
    system_navigation_bar_icon_brightness: Optional[Brightness] = None
    status_bar_brightness: Optional[Brightness] = None
    status_bar_icon_brightness: Optional[Brightness] = None


@dataclass
class DialogTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    title_text_style: Optional[TextStyle] = None
    content_text_style: Optional[TextStyle] = None
    alignment: Optional[Alignment] = None
    actions_padding: Optional[PaddingValue] = None


@dataclass
class BottomSheetTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    drag_handle_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    show_drag_handle: Optional[bool] = None
    modal_bgcolor: Optional[ColorValue] = None
    modal_elevation: OptionalNumber = None
    clip_behavior: Optional[ClipBehavior] = None


@dataclass
class CardTheme:
    color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    clip_behavior: Optional[ClipBehavior] = None
    margin: MarginValue = None


@dataclass
class ChipTheme:
    # color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    disabled_color: Optional[ColorValue] = None
    selected_color: Optional[ColorValue] = None
    checkmark_color: Optional[ColorValue] = None
    delete_icon_color: Optional[ColorValue] = None
    secondary_selected_color: Optional[ColorValue] = None
    selected_shadow_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    click_elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    padding: PaddingValue = None
    label_padding: PaddingValue = None
    label_text_style: Optional[TextStyle] = None
    secondary_label_text_style: Optional[TextStyle] = None
    border_side: Optional[BorderSide] = None
    brightness: Optional[Brightness] = None
    show_checkmark: Optional[bool] = None


@dataclass
class FloatingActionButtonTheme:
    bgcolor: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    foreground_color: Optional[ColorValue] = None
    splash_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    focus_elevation: OptionalNumber = None
    hover_elevation: OptionalNumber = None
    highlight_elevation: OptionalNumber = None
    disabled_elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    enable_feedback: Optional[bool] = None
    extended_padding: PaddingValue = None
    extended_text_style: Optional[TextStyle] = None
    extended_icon_label_spacing: OptionalNumber = None


@dataclass
class NavigationRailTheme:
    bgcolor: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    indicator_shape: Optional[OutlinedBorder] = None
    unselected_label_text_style: Optional[TextStyle] = None
    selected_label_text_style: Optional[TextStyle] = None
    label_type: Optional[NavigationRailLabelType] = None
    min_width: OptionalNumber = None
    min_extended_width: OptionalNumber = None
    group_alignment: OptionalNumber = None
    use_indicator: Optional = None


@dataclass
class AppBarTheme:
    color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    foreground_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    title_text_style: Optional[TextStyle] = None
    toolbar_text_style: Optional[TextStyle] = None
    center_title: Optional[bool] = None
    title_spacing: OptionalNumber = None
    scroll_elevation: OptionalNumber = None
    toolbar_height: OptionalNumber = None


@dataclass
class BottomAppBarTheme:
    color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    height: OptionalNumber = None
    padding: PaddingValue = None


@dataclass
class RadioTheme:
    fill_color: ControlStateValue[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    splash_radius: OptionalNumber = None
    height: OptionalNumber = None
    visual_density: Union[None, ThemeVisualDensity, VisualDensity] = None
    mouse_cursor: ControlStateValue[MouseCursor] = None


@dataclass
class CheckboxTheme:
    overlay_color: ControlStateValue[ColorValue] = None
    check_color: ControlStateValue[ColorValue] = None
    fill_color: ControlStateValue[ColorValue] = None
    splash_radius: OptionalNumber = None
    border_side: Optional[BorderSide] = None
    visual_density: Union[None, ThemeVisualDensity, VisualDensity] = None
    shape: Optional[OutlinedBorder] = None
    mouse_cursor: ControlStateValue[MouseCursor] = None


@dataclass
class BadgeTheme:
    bgcolor: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    small_size: OptionalNumber = None
    large_size: OptionalNumber = None
    alignment: Optional[Alignment] = None
    padding: PaddingValue = None
    offset: OffsetValue = None
    text_style: Optional[TextStyle] = None


@dataclass
class SwitchTheme:
    thumb_color: ControlStateValue[ColorValue] = None
    track_color: ControlStateValue[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    track_outline_color: ControlStateValue[ColorValue] = None
    thumb_icon: ControlStateValue[str] = None
    track_outline_width: ControlStateValue[OptionalNumber] = None
    splash_radius: OptionalNumber = None
    mouse_cursor: ControlStateValue[MouseCursor] = None


@dataclass
class DividerTheme:
    color: Optional[ColorValue] = None
    thickness: OptionalNumber = None
    space: OptionalNumber = None
    leading_indent: OptionalNumber = None
    trailing_indent: OptionalNumber = None


@dataclass
class SnackBarTheme:
    bgcolor: Optional[ColorValue] = None
    action_text_color: Optional[ColorValue] = None
    action_bgcolor: Optional[ColorValue] = None
    close_icon_color: Optional[ColorValue] = None
    disabled_action_text_color: Optional[ColorValue] = None
    disabled_action_bgcolor: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    content_text_style: Optional[TextStyle] = None
    width: OptionalNumber = None
    alignment: Optional[Alignment] = None
    show_close_icon: Optional[bool] = None
    dismiss_direction: Optional[DismissDirection] = None
    behavior: Optional[SnackBarBehavior] = None
    shape: Optional[OutlinedBorder] = None
    inset_padding: PaddingValue = None
    action_overflow_threshold: OptionalNumber = None


@dataclass
class BannerTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    padding: PaddingValue = None
    leading_padding: PaddingValue = None
    elevation: OptionalNumber = None
    content_text_style: Optional[TextStyle] = None


@dataclass
class DatePickerTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    header_bgcolor: Optional[ColorValue] = None
    today_bgcolor: ControlStateValue[ColorValue] = None
    day_bgcolor: ControlStateValue[ColorValue] = None
    day_overlay_color: ControlStateValue[ColorValue] = None
    day_foreground_color: ControlStateValue[ColorValue] = None
    elevation: OptionalNumber = None
    range_picker_elevation: OptionalNumber = None
    day_text_style: Optional[TextStyle] = None
    weekday_text_style: Optional[TextStyle] = None
    year_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None
    cancel_button_style: Optional[ButtonStyle] = None
    confirm_button_style: Optional[ButtonStyle] = None
    header_foreground_color: Optional[ColorValue] = None
    header_headline_text_style: Optional[TextStyle] = None
    header_help_text_style: Optional[TextStyle] = None
    range_picker_bgcolor: Optional[ColorValue] = None
    range_picker_header_bgcolor: Optional[ColorValue] = None
    range_picker_header_foreground_color: Optional[ColorValue] = None
    today_foreground_color: ControlStateValue[ColorValue] = None
    range_picker_shape: Optional[OutlinedBorder] = None
    range_picker_header_help_text_style: Optional[TextStyle] = None
    range_picker_header_headline_text_style: Optional[TextStyle] = None
    range_picker_surface_tint_color: Optional[ColorValue] = None
    range_selection_bgcolor: Optional[ColorValue] = None
    range_selection_overlay_color: ControlStateValue[ColorValue] = None
    today_border_side: Optional[BorderSide] = None
    year_bgcolor: ControlStateValue[ColorValue] = None
    year_foreground_color: ControlStateValue[ColorValue] = None
    year_overlay_color: ControlStateValue[ColorValue] = None


@dataclass
class TimePickerTheme:
    bgcolor: Optional[ColorValue] = None
    day_period_color: Optional[ColorValue] = None
    day_period_text_color: Optional[ColorValue] = None
    dial_bgcolor: Optional[ColorValue] = None
    dial_hand_color: Optional[ColorValue] = None
    dial_text_color: Optional[ColorValue] = None
    entry_mode_icon_color: Optional[ColorValue] = None
    hour_minute_color: Optional[ColorValue] = None
    hour_minute_text_color: Optional[ColorValue] = None
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
    padding: PaddingValue = None


# @dataclass
# class DropdownMenuTheme:
#     menu_style: Optional[MenuStyle] = None
#     text_style: Optional[TextStyle] = None


@dataclass
class ListTileTheme:
    icon_color: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    selected_tile_color: Optional[ColorValue] = None
    selected_color: Optional[ColorValue] = None
    is_three_line: Optional[bool] = None
    enable_feedback: Optional[bool] = None
    dense: Optional[bool] = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Union[None, ThemeVisualDensity, VisualDensity] = None
    content_padding: PaddingValue = None
    min_vertical_padding: PaddingValue = None
    horizontal_spacing: OptionalNumber = None
    min_leading_width: OptionalNumber = None
    title_text_style: Optional[TextStyle] = None
    subtitle_text_style: Optional[TextStyle] = None
    leading_and_trailing_text_style: Optional[TextStyle] = None


@dataclass
class TooltipTheme:
    height: OptionalNumber = None
    text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    exclude_from_semantics: Optional[bool] = None


@dataclass
class ExpansionTileTheme:
    bgcolor: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    collapsed_bgcolor: Optional[ColorValue] = None
    collapsed_icon_color: Optional[ColorValue] = None


@dataclass
class SliderTheme:
    active_track_color: Optional[ColorValue] = None
    inactive_track_color: Optional[ColorValue] = None
    thumb_color: Optional[ColorValue] = None
    overlay_color: Optional[ColorValue] = None
    value_indicator_color: Optional[ColorValue] = None
    disabled_thumb_color: Optional[ColorValue] = None
    value_indicator_text_style: Optional[TextStyle] = None


@dataclass
class ProgressIndicatorTheme:
    color: Optional[ColorValue] = None
    circular_track_color: Optional[ColorValue] = None
    linear_track_color: Optional[ColorValue] = None
    refresh_bgcolor: Optional[ColorValue] = None
    linear_min_height: OptionalNumber = None


@dataclass
class PopupMenuTheme:
    color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    text_style: Optional[TextStyle] = None
    label_text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    elevation: OptionalNumber = None
    icon_size: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    menu_position: Optional[PopupMenuPosition] = None
    mouse_cursor: ControlStateValue[MouseCursor] = None


@dataclass
class SearchBarTheme:
    bgcolor: Optional[ColorValue] = None
    text_capitalization: Optional[TextCapitalization] = None
    shadow_color: ControlStateValue[ColorValue] = None
    surface_tint_color: ControlStateValue[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    elevation: ControlStateValue[OptionalNumber] = None
    text_style: ControlStateValue[TextStyle] = None
    hint_style: ControlStateValue[TextStyle] = None
    shape: ControlStateValue[OutlinedBorder] = None
    padding: ControlStateValue[PaddingValue] = None

    def __post_init__(self):
        if not isinstance(self.text_style, dict):
            self.text_style = {ControlState.DEFAULT: self.text_style}
        if not isinstance(self.hint_style, dict):
            self.hint_style = {ControlState.DEFAULT: self.hint_style}
        if not isinstance(self.shape, dict):
            self.shape = {ControlState.DEFAULT: self.shape}
        if not isinstance(self.padding, dict):
            self.padding = {ControlState.DEFAULT: self.padding}


@dataclass
class SearchViewTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    header_hint_text_style: Optional[TextStyle] = None
    header_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None
    border_side: Optional[BorderSide] = None


@dataclass
class BottomNavigationBarTheme:
    bgcolor: Optional[ColorValue] = None
    selected_item_color: Optional[ColorValue] = None
    unselected_item_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    enable_feedback: Optional[bool] = None
    show_selected_labels: Optional[bool] = None
    show_unselected_labels: Optional[bool] = None
    selected_label_text_style: Optional[TextStyle] = None
    unselected_label_text_style: Optional[TextStyle] = None


@dataclass
class NavigationDrawerTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    tile_height: OptionalNumber = None
    label_text_style: ControlStateValue[TextStyle] = None
    indicator_shape: Optional[OutlinedBorder] = None

    def __post_init__(self):
        if not isinstance(self.label_text_style, dict):
            self.label_text_style = {ControlState.DEFAULT: self.label_text_style}


@dataclass
class NavigationBarTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    elevation: OptionalNumber = None
    height: OptionalNumber = None
    label_text_style: ControlStateValue[TextStyle] = None
    indicator_shape: Optional[OutlinedBorder] = None
    label_behavior: Optional[NavigationBarLabelBehavior] = None

    def __post_init__(self):
        if not isinstance(self.label_text_style, dict):
            self.label_text_style = {ControlState.DEFAULT: self.label_text_style}


@dataclass
class SegmentedButtonTheme:
    # selected_icon: Optional[IconValue] = None
    style: Optional[ButtonStyle] = None


@dataclass
class IconTheme:
    color: Optional[ColorValue] = None
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
class ButtonTheme:
    button_color: Optional[ColorValue] = None
    disabled_color: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    highlight_color: Optional[ColorValue] = None
    splash_color: Optional[ColorValue] = None
    color_scheme: Optional[ColorScheme] = None
    aligned_dropdown: Optional[bool] = None
    height: OptionalNumber = None
    min_width: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    padding: PaddingValue = None


@dataclass
class Theme:
    color_scheme_seed: Optional[str] = None
    primary_swatch: Optional[str] = None
    font_family: Optional[str] = None
    use_material3: Optional[bool] = None
    appbar_theme: Optional[AppBarTheme] = None
    badge_theme: Optional[BadgeTheme] = None
    banner_theme: Optional[BannerTheme] = None
    bottom_appbar_theme: Optional[BottomAppBarTheme] = None
    bottom_navigation_bar_theme: Optional[BottomNavigationBarTheme] = None
    bottom_sheet_theme: Optional[BottomSheetTheme] = None
    button_theme: Optional[ButtonTheme] = None
    card_theme: Optional[CardTheme] = None
    checkbox_theme: Optional[CheckboxTheme] = None
    chip_theme: Optional[ChipTheme] = None
    color_scheme: Optional[ColorScheme] = None
    data_table_theme: Optional[DataTableTheme] = None
    date_picker_theme: Optional[DatePickerTheme] = None
    dialog_theme: Optional[DialogTheme] = None
    divider_theme: Optional[DividerTheme] = None
    # dropdown_menu_theme: Optional[DropdownMenuTheme] = None
    expansion_tile_theme: Optional[ExpansionTileTheme] = None
    floating_action_button_theme: Optional[FloatingActionButtonTheme] = None
    icon_theme: Optional[IconTheme] = None
    list_tile_theme: Optional[ListTileTheme] = None
    navigation_bar_theme: Optional[NavigationBarTheme] = None
    navigation_drawer_theme: Optional[NavigationDrawerTheme] = None
    navigation_rail_theme: Optional[NavigationRailTheme] = None
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
    popup_menu_theme: Optional[PopupMenuTheme] = None
    primary_color: Optional[ColorValue] = None
    primary_color_dark: Optional[str] = None
    primary_color_light: Optional[str] = None
    primary_text_theme: Optional[TextTheme] = None
    progress_indicator_theme: Optional[ProgressIndicatorTheme] = None
    radio_theme: Optional[RadioTheme] = None
    scrollbar_theme: Optional[ScrollbarTheme] = None
    search_bar_theme: Optional[SearchBarTheme] = None
    # search_view_theme: Optional[SearchViewTheme] = None
    segmented_button_theme: Optional[SegmentedButtonTheme] = None
    slider_theme: Optional[SliderTheme] = None
    snackbar_theme: Optional[SnackBarTheme] = None
    switch_theme: Optional[SwitchTheme] = None
    system_overlay_style: SystemOverlayStyle = field(default_factory=SystemOverlayStyle)
    tabs_theme: Optional[TabsTheme] = None
    text_theme: Optional[TextTheme] = None
    time_picker_theme: Optional[TimePickerTheme] = None
    tooltip_theme: Optional[TooltipTheme] = None
    visual_density: Union[VisualDensity, ThemeVisualDensity] = field(
        default=VisualDensity.STANDARD
    )
