from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.box import BoxConstraints, BoxDecoration, BoxShadow
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import DurationValue
from flet.controls.geometry import Size
from flet.controls.margin import MarginValue
from flet.controls.material.menu_bar import MenuStyle
from flet.controls.material.navigation_bar import NavigationBarLabelBehavior
from flet.controls.material.navigation_rail import NavigationRailLabelType
from flet.controls.material.popup_menu_button import PopupMenuPosition
from flet.controls.material.slider import SliderInteraction
from flet.controls.material.snack_bar import DismissDirection, SnackBarBehavior
from flet.controls.material.textfield import TextCapitalization
from flet.controls.material.tooltip import TooltipTriggerMode
from flet.controls.padding import PaddingValue
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
    Number,
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
    """
    A set of more than 40 colors based on the [Material spec](https://m3.material.io/styles/color/the-color-system/color-roles)
    that can be used to configure the color properties of most components.
    Read more about color schemes in [here](https://api.flutter.dev/flutter/material/ColorScheme-class.html).
    """

    primary: Optional[ColorValue] = None
    """
    The color displayed most frequently across your app’s screens and components.
    """
    on_primary: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `primary`.
    """
    primary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than `primary`.
    """
    on_primary_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `primary_container`.
    """
    secondary: Optional[ColorValue] = None
    """
    An accent color used for less prominent components in the UI, such as filter chips,
    while expanding the opportunity for color expression.
    """
    on_secondary: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `secondary`.
    """
    secondary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than `secondary`.
    """
    on_secondary_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `secondary_container`.
    """
    tertiary: Optional[ColorValue] = None
    """
    A color used as a contrasting accent that can balance `primary` and `secondary`
    colors or bring heightened attention to an element, such as an input field.
    """
    on_tertiary: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `tertiary`.
    """
    tertiary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than `tertiary`.
    """
    on_tertiary_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `tertiary_container`.
    """
    error: Optional[ColorValue] = None
    """
    The color to use for input validation errors, e.g. for `TextField.error_text`.
    """
    on_error: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `error`.
    """
    error_container: Optional[ColorValue] = None
    """
    A color used for error elements needing less emphasis than `error`.
    """
    on_error_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `error_container`.
    """
    background: Optional[ColorValue] = None
    """
    A color that typically appears behind scrollable content.
    """
    on_background: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `background`.
    """
    surface: Optional[ColorValue] = None
    """
    The background color for widgets like `Card`.
    """
    on_surface: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `surface`.
    """
    surface_variant: Optional[ColorValue] = None
    """
    A color variant of `surface` that can be used for differentiation against a
    component using `surface`.
    """
    on_surface_variant: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `surface_variant`.
    """
    outline: Optional[ColorValue] = None
    """
    A utility color that creates boundaries and emphasis to improve usability.
    """
    outline_variant: Optional[ColorValue] = None
    """
    A utility color that creates boundaries for decorative elements when a 3:1 contrast
    isn’t required, such as for dividers or decorative elements.
    """
    shadow: Optional[ColorValue] = None
    """
    A color use to paint the drop shadows of elevated components.
    """
    scrim: Optional[ColorValue] = None
    """
    A color use to paint the scrim around of modal components.
    """
    inverse_surface: Optional[ColorValue] = None
    """
    A surface color used for displaying the reverse of what’s seen in the surrounding
    UI, for example in a `SnackBar` to bring attention to an alert.
    """
    on_inverse_surface: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `inverse_surface`.
    """
    inverse_primary: Optional[ColorValue] = None
    """
    An accent color used for displaying a highlight color on `inverse_surface`
    backgrounds, like button text in a `SnackBar`.
    """
    surface_tint: Optional[ColorValue] = None
    """
    A color used as an overlay on a surface color to indicate a component's elevation.
    """
    on_primary_fixed: Optional[ColorValue] = None
    """
    A color that is used for text and icons that exist on top of elements having
    `primary_fixed` color.
    """
    on_secondary_fixed: Optional[ColorValue] = None
    """
    A color that is used for text and icons that exist on top of elements having
    `secondary_fixed` color.
    """
    on_tertiary_fixed: Optional[ColorValue] = None
    """
    A color that is used for text and icons that exist on top of elements having
    `tertiary_fixed` color.
    """
    on_primary_fixed_variant: Optional[ColorValue] = None
    """
    A color that provides a lower-emphasis option for text and icons than
    `on_primary_fixed`.
    """
    on_secondary_fixed_variant: Optional[ColorValue] = None
    """
    A color that provides a lower-emphasis option for text and icons than
    `on_secondary_fixed`.
    """
    on_tertiary_fixed_variant: Optional[ColorValue] = None
    """
    A color that provides a lower-emphasis option for text and icons than
    `on_tertiary_fixed`.
    """
    primary_fixed: Optional[ColorValue] = None
    """
    A substitute for `primary_container` that's the same color for the dark and light
    themes.
    """
    secondary_fixed: Optional[ColorValue] = None
    """
    A substitute for `secondary_container` that's the same color for the dark and light
    themes.
    """
    tertiary_fixed: Optional[ColorValue] = None
    """
    A substitute for `tertiary_container` that's the same color for dark and light
    themes.
    """
    primary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than `primary_fixed`.
    """
    secondary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than `secondary_fixed`.
    """
    surface_bright: Optional[ColorValue] = None
    """
    A color that's always the lightest in the dark or light theme.
    """
    surface_container: Optional[ColorValue] = None
    surface_container_high: Optional[ColorValue] = None
    surface_container_low: Optional[ColorValue] = None
    surface_container_lowest: Optional[ColorValue] = None
    surface_dim: Optional[ColorValue] = None
    tertiary_fixed_dim: Optional[ColorValue] = None


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
    thumb_visibility: Optional[ControlStateValue[bool]] = None
    thickness: Optional[ControlStateValue[Optional[Number]]] = None
    track_visibility: Optional[ControlStateValue[bool]] = None
    radius: Optional[Number] = None
    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    track_color: Optional[ControlStateValue[ColorValue]] = None
    track_border_color: Optional[ControlStateValue[ColorValue]] = None
    cross_axis_margin: Optional[Number] = None
    main_axis_margin: Optional[Number] = None
    min_thumb_length: Optional[Number] = None
    interactive: Optional[bool] = None


@dataclass
class TabsTheme:
    divider_color: Optional[ColorValue] = None
    indicator_border_radius: Optional[BorderRadiusValue] = None
    indicator_border_side: Optional[BorderSide] = None
    indicator_padding: Optional[PaddingValue] = None
    indicator_color: Optional[ColorValue] = None
    indicator_tab_size: Optional[bool] = None
    label_color: Optional[ColorValue] = None
    unselected_label_color: Optional[ColorValue] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    mouse_cursor: Optional[ControlStateValue[Optional[MouseCursor]]] = None
    label_padding: Optional[PaddingValue] = None
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
    elevation: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    title_text_style: Optional[TextStyle] = None
    content_text_style: Optional[TextStyle] = None
    alignment: Optional[Alignment] = None
    actions_padding: Optional[PaddingValue] = None
    clip_behavior: Optional[ClipBehavior] = None
    barrier_color: Optional[ColorValue] = None
    inset_padding: Optional[PaddingValue] = None


@dataclass
class ElevatedButtonTheme:
    bgcolor: Optional[ColorValue] = None
    foreground_color: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    disabled_bgcolor: Optional[ColorValue] = None
    disabled_foreground_color: Optional[ColorValue] = None
    disabled_icon_color: Optional[ColorValue] = None
    overlay_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    padding: Optional[PaddingValue] = None
    enable_feedback: Optional[bool] = None
    disabled_mouse_cursor: Optional[MouseCursor] = None
    enabled_mouse_cursor: Optional[MouseCursor] = None
    shape: Optional[OutlinedBorder] = None
    text_style: Optional[TextStyle] = None
    visual_density: Optional[VisualDensity] = None
    border_side: Optional[BorderSide] = None
    animation_duration: Optional[DurationValue] = None
    alignment: Optional[Alignment] = None
    icon_size: Optional[Number] = None
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
    bgcolor: Optional[ColorValue] = None
    foreground_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    disabled_bgcolor: Optional[ColorValue] = None
    disabled_foreground_color: Optional[ColorValue] = None
    overlay_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    padding: Optional[PaddingValue] = None
    enable_feedback: Optional[bool] = None
    disabled_mouse_cursor: Optional[MouseCursor] = None
    enabled_mouse_cursor: Optional[MouseCursor] = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Optional[VisualDensity] = None
    border_side: Optional[BorderSide] = None
    animation_duration: Optional[DurationValue] = None
    alignment: Optional[Alignment] = None
    icon_size: Optional[Number] = None
    fixed_size: Optional[Size] = None
    maximum_size: Optional[Size] = None
    minimum_size: Optional[Size] = None
    # Icon Button Theme
    focus_color: Optional[ColorValue] = None
    highlight_color: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None


@dataclass
class BottomSheetTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    drag_handle_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    show_drag_handle: Optional[bool] = None
    modal_bgcolor: Optional[ColorValue] = None
    modal_elevation: Optional[Number] = None
    clip_behavior: Optional[ClipBehavior] = None
    size_constraints: Optional[BoxConstraints] = None
    modal_barrier_color: Optional[ColorValue] = None


@dataclass
class CardTheme:
    color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    clip_behavior: Optional[ClipBehavior] = None
    margin: Optional[MarginValue] = None


@dataclass
class ChipTheme:
    color: Optional[ControlStateValue[ColorValue]] = None
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    disabled_color: Optional[ColorValue] = None
    selected_color: Optional[ColorValue] = None
    checkmark_color: Optional[ColorValue] = None
    delete_icon_color: Optional[ColorValue] = None
    secondary_selected_color: Optional[ColorValue] = None
    selected_shadow_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    click_elevation: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    padding: Optional[PaddingValue] = None
    label_padding: Optional[PaddingValue] = None
    label_text_style: Optional[TextStyle] = None
    secondary_label_text_style: Optional[TextStyle] = None
    border_side: Optional[BorderSide] = None
    brightness: Optional[Brightness] = None
    show_checkmark: Optional[bool] = None
    avatar_constraints: Optional[BoxConstraints] = None
    delete_icon_size_constraints: Optional[BoxConstraints] = None


@dataclass
class FloatingActionButtonTheme:
    bgcolor: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    foreground_color: Optional[ColorValue] = None
    splash_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    focus_elevation: Optional[Number] = None
    hover_elevation: Optional[Number] = None
    highlight_elevation: Optional[Number] = None
    disabled_elevation: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    enable_feedback: Optional[bool] = None
    extended_padding: Optional[PaddingValue] = None
    extended_text_style: Optional[TextStyle] = None
    extended_icon_label_spacing: Optional[Number] = None
    extended_size_constraints: Optional[BoxConstraints] = None
    size_constraints: Optional[BoxConstraints] = None
    large_size_constraints: Optional[BoxConstraints] = None
    small_size_constraints: Optional[BoxConstraints] = None


@dataclass
class NavigationRailTheme:
    bgcolor: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    indicator_shape: Optional[OutlinedBorder] = None
    unselected_label_text_style: Optional[TextStyle] = None
    selected_label_text_style: Optional[TextStyle] = None
    label_type: Optional[NavigationRailLabelType] = None
    min_width: Optional[Number] = None
    min_extended_width: Optional[Number] = None
    group_alignment: Optional[Number] = None
    use_indicator: Optional[bool] = None


@dataclass
class AppBarTheme:
    """
    Customizes the appearance of [`AppBar`][flet.AppBar] controls across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of `AppBar.color` in all descendant `AppBar` controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of `AppBar.bgcolor` in all descendant `AppBar` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of `AppBar.shadow_color` in all descendant `AppBar`
    controls.
    """

    surface_tint_color: Optional[ColorValue] = None
    """
    Overrides the default value of `AppBar.surface_tint_color` in all descendant
    `AppBar` controls.
    """

    foreground_color: Optional[ColorValue] = None
    """
    TBD
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of `AppBar.elevation` in all descendant `AppBar`
    controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of `AppBar.shape` in all descendant `AppBar` controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of `AppBar.title_text_style` in all descendant
    `AppBar` controls.
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of `AppBar.toolbar_text_style` in all descendant
    `AppBar` controls.
    """

    center_title: Optional[bool] = None
    """
    Overrides the default value of `AppBar.center_title` in all descendant `AppBar`
    controls.
    """

    title_spacing: Optional[Number] = None
    """
    Overrides the default value of `AppBar.title_spacing` in all descendant `AppBar`
    controls.
    """

    scroll_elevation: Optional[Number] = None
    """
    Overrides the default value of `AppBar.scroll_elevation` in all descendant
    `AppBar` controls.
    """

    toolbar_height: Optional[Number] = None
    """
    Overrides the default value of `AppBar.toolbar_height` in all descendant `AppBar`
    controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    TBD
    """


@dataclass
class BottomAppBarTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    height: Optional[Number] = None
    padding: Optional[PaddingValue] = None
    shape: Optional[NotchShape] = None


@dataclass
class RadioTheme:
    fill_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    splash_radius: Optional[Number] = None
    height: Optional[Number] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class CheckboxTheme:
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    check_color: Optional[ControlStateValue[ColorValue]] = None
    fill_color: Optional[ControlStateValue[ColorValue]] = None
    splash_radius: Optional[Number] = None
    border_side: Optional[BorderSide] = None
    visual_density: Optional[VisualDensity] = None
    shape: Optional[OutlinedBorder] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class BadgeTheme:
    bgcolor: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    small_size: Optional[Number] = None
    large_size: Optional[Number] = None
    alignment: Optional[Alignment] = None
    padding: Optional[PaddingValue] = None
    offset: Optional[OffsetValue] = None
    text_style: Optional[TextStyle] = None


@dataclass
class SwitchTheme:
    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    track_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    thumb_icon: Optional[ControlStateValue[IconValue]] = None
    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    splash_radius: Optional[Number] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    padding: Optional[PaddingValue] = None


@dataclass
class DividerTheme:
    color: Optional[ColorValue] = None
    thickness: Optional[Number] = None
    space: Optional[Number] = None
    leading_indent: Optional[Number] = None
    trailing_indent: Optional[Number] = None


@dataclass
class SnackBarTheme:
    bgcolor: Optional[ColorValue] = None
    action_text_color: Optional[ColorValue] = None
    action_bgcolor: Optional[ColorValue] = None
    close_icon_color: Optional[ColorValue] = None
    disabled_action_text_color: Optional[ColorValue] = None
    disabled_action_bgcolor: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    content_text_style: Optional[TextStyle] = None
    width: Optional[Number] = None
    alignment: Optional[Alignment] = None
    show_close_icon: Optional[bool] = None
    dismiss_direction: Optional[DismissDirection] = None
    behavior: Optional[SnackBarBehavior] = None
    shape: Optional[OutlinedBorder] = None
    inset_padding: Optional[PaddingValue] = None
    action_overflow_threshold: Optional[Number] = None


@dataclass
class BannerTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    padding: Optional[PaddingValue] = None
    leading_padding: Optional[PaddingValue] = None
    elevation: Optional[Number] = None
    content_text_style: Optional[TextStyle] = None


@dataclass
class DatePickerTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    header_bgcolor: Optional[ColorValue] = None
    today_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    day_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    day_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    day_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[Number] = None
    range_picker_elevation: Optional[Number] = None
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
    today_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    range_picker_shape: Optional[OutlinedBorder] = None
    range_picker_header_help_text_style: Optional[TextStyle] = None
    range_picker_header_headline_text_style: Optional[TextStyle] = None
    range_picker_surface_tint_color: Optional[ColorValue] = None
    range_selection_bgcolor: Optional[ColorValue] = None
    range_selection_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    today_border_side: Optional[BorderSide] = None
    year_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    year_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    year_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    day_shape: Optional[ControlStateValue[OutlinedBorder]] = None
    locale: Optional[Locale] = None


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
    elevation: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    day_period_shape: Optional[OutlinedBorder] = None
    hour_minute_shape: Optional[OutlinedBorder] = None
    day_period_border_side: Optional[BorderSide] = None
    padding: Optional[PaddingValue] = None
    time_selector_separator_color: Optional[ControlStateValue[ColorValue]] = None
    time_selector_separator_text_style: Optional[ControlStateValue[TextStyle]] = None


@dataclass
class DropdownTheme:
    menu_style: Optional[MenuStyle] = None
    text_style: Optional[TextStyle] = None


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
    visual_density: Optional[VisualDensity] = None
    content_padding: Optional[PaddingValue] = None
    min_vertical_padding: Optional[PaddingValue] = None
    horizontal_spacing: Optional[Number] = None
    min_leading_width: Optional[Number] = None
    title_text_style: Optional[TextStyle] = None
    subtitle_text_style: Optional[TextStyle] = None
    leading_and_trailing_text_style: Optional[TextStyle] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    min_tile_height: Optional[Number] = None


@dataclass
class TooltipTheme:
    text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    exclude_from_semantics: Optional[bool] = None
    prefer_below: Optional[bool] = None
    vertical_offset: Optional[Number] = None
    padding: Optional[PaddingValue] = None
    wait_duration: Optional[DurationValue] = None
    exit_duration: Optional[DurationValue] = None
    show_duration: Optional[DurationValue] = None
    margin: Optional[MarginValue] = None
    trigger_mode: Optional[TooltipTriggerMode] = None
    decoration: Optional[BoxDecoration] = None
    text_align: Optional[TextAlign] = None
    size_constraints: Optional[BoxConstraints] = None


@dataclass
class ExpansionTileTheme:
    bgcolor: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    collapsed_bgcolor: Optional[ColorValue] = None
    collapsed_icon_color: Optional[ColorValue] = None
    clip_behavior: Optional[ClipBehavior] = None
    collapsed_text_color: Optional[ColorValue] = None
    tile_padding: Optional[PaddingValue] = None
    expanded_alignment: Optional[Alignment] = None
    controls_padding: Optional[PaddingValue] = None


@dataclass
class SliderTheme:
    active_track_color: Optional[ColorValue] = None
    inactive_track_color: Optional[ColorValue] = None
    thumb_color: Optional[ColorValue] = None
    overlay_color: Optional[ColorValue] = None
    value_indicator_color: Optional[ColorValue] = None
    disabled_thumb_color: Optional[ColorValue] = None
    value_indicator_text_style: Optional[TextStyle] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    active_tick_mark_color: Optional[ColorValue] = None
    disabled_active_tick_mark_color: Optional[ColorValue] = None
    disabled_active_track_color: Optional[ColorValue] = None
    disabled_inactive_tick_mark_color: Optional[ColorValue] = None
    disabled_inactive_track_color: Optional[ColorValue] = None
    disabled_secondary_active_track_color: Optional[ColorValue] = None
    inactive_tick_mark_color: Optional[ColorValue] = None
    overlapping_shape_stroke_color: Optional[ColorValue] = None
    min_thumb_separation: Optional[Number] = None
    secondary_active_track_color: Optional[ColorValue] = None
    track_height: Optional[Number] = None
    value_indicator_stroke_color: Optional[ColorValue] = None
    interaction: Optional[SliderInteraction] = None
    padding: Optional[PaddingValue] = None
    track_gap: Optional[Number] = None
    thumb_size: Optional[ControlStateValue[Size]] = None
    year_2023: Optional[bool] = None


@dataclass
class ProgressIndicatorTheme:
    color: Optional[ColorValue] = None
    circular_track_color: Optional[ColorValue] = None
    linear_track_color: Optional[ColorValue] = None
    refresh_bgcolor: Optional[ColorValue] = None
    linear_min_height: Optional[Number] = None
    border_radius: Optional[BorderRadiusValue] = None
    track_gap: Optional[Number] = None
    circular_track_padding: Optional[PaddingValue] = None
    size_constraints: Optional[BoxConstraints] = None
    stop_indicator_color: Optional[ColorValue] = None
    stop_indicator_radius: Optional[Number] = None
    stroke_align: Optional[Number] = None
    stroke_cap: Optional[StrokeCap] = None
    stroke_width: Optional[Number] = None
    year_2023: Optional[bool] = None


@dataclass
class PopupMenuTheme:
    color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    text_style: Optional[TextStyle] = None
    label_text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    elevation: Optional[Number] = None
    icon_size: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    menu_position: Optional[PopupMenuPosition] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    menu_padding: Optional[PaddingValue] = None


@dataclass
class SearchBarTheme:
    bgcolor: Optional[ColorValue] = None
    text_capitalization: Optional[TextCapitalization] = None
    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    surface_tint_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[ControlStateValue[Optional[Number]]] = None
    text_style: Optional[ControlStateValue[TextStyle]] = None
    hint_style: Optional[ControlStateValue[TextStyle]] = None
    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    padding: Optional[ControlStateValue[PaddingValue]] = None
    size_constraints: Optional[BoxConstraints] = None
    border_side: Optional[ControlStateValue[BorderSide]] = None


@dataclass
class SearchViewTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    header_hint_text_style: Optional[TextStyle] = None
    header_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None
    border_side: Optional[BorderSide] = None
    size_constraints: Optional[BoxConstraints] = None
    header_height: Optional[Number] = None
    padding: Optional[PaddingValue] = None
    bar_padding: Optional[PaddingValue] = None
    shrink_wrap: Optional[bool] = None


@dataclass
class NavigationDrawerTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    tile_height: Optional[Number] = None
    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    indicator_shape: Optional[OutlinedBorder] = None
    indicator_size: Optional[Size] = None


@dataclass
class NavigationBarTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[Number] = None
    height: Optional[Number] = None
    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    indicator_shape: Optional[OutlinedBorder] = None
    label_behavior: Optional[NavigationBarLabelBehavior] = None
    label_padding: Optional[PaddingValue] = None


@dataclass
class SegmentedButtonTheme:
    selected_icon: Optional[IconValue] = None
    style: Optional[ButtonStyle] = None


@dataclass
class IconTheme:
    color: Optional[ColorValue] = None
    apply_text_scaling: Optional[bool] = None
    fill: Optional[Number] = None
    opacity: Optional[Number] = None
    size: Optional[Number] = None
    optical_size: Optional[Number] = None
    grade: Optional[Number] = None
    weight: Optional[Number] = None
    shadows: Optional[list[BoxShadow]] = None


@dataclass
class DataTableTheme:
    checkbox_horizontal_margin: Optional[Number] = None
    column_spacing: Optional[Number] = None
    data_row_max_height: Optional[Number] = None
    data_row_min_height: Optional[Number] = None
    data_row_color: Optional[ControlStateValue[ColorValue]] = None
    data_text_style: Optional[TextStyle] = None
    divider_thickness: Optional[Number] = None
    horizontal_margin: Optional[Number] = None
    heading_text_style: Optional[TextStyle] = None
    heading_row_color: Optional[ControlStateValue[ColorValue]] = None
    heading_row_height: Optional[Number] = None
    data_row_cursor: Optional[ControlStateValue[MouseCursor]] = None
    decoration: Optional[BoxDecoration] = None
    heading_row_alignment: Optional[MainAxisAlignment] = None
    heading_cell_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class Theme:
    color_scheme_seed: Optional[ColorValue] = None
    primary_swatch: Optional[ColorValue] = None
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
    dropdown_theme: Optional[DropdownTheme] = None
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
    splash_color: Optional[ColorValue] = None
    highlight_color: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    unselected_control_color: Optional[ColorValue] = None
    disabled_color: Optional[ColorValue] = None
    canvas_color: Optional[ColorValue] = None
    scaffold_bgcolor: Optional[ColorValue] = None
    card_bgcolor: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    hint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    secondary_header_color: Optional[ColorValue] = None
    primary_color: Optional[ColorValue] = None
    primary_color_dark: Optional[ColorValue] = None
    primary_color_light: Optional[ColorValue] = None
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
