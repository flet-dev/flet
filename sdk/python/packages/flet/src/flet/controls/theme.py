from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide, OptionalBorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.box import BoxConstraints, BoxDecoration, BoxShadow
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.control_state import ControlStateValue
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
from flet.controls.geometry import Size
from flet.controls.text_style import OptionalTextStyle, TextStyle
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
    OptionalBool,
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
    """
    A set of more than 40 colors based on the [Material spec](https://m3.material.io/styles/color/the-color-system/color-roles) 
    that can be used to configure the color properties of most components. 
    Read more about color schemes in [here](https://api.flutter.dev/flutter/material/ColorScheme-class.html).
    """
    primary: OptionalColorValue = None
    """
    The color displayed most frequently across your app’s screens and components.
    """
    on_primary: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `primary`.
    """
    primary_container: OptionalColorValue = None
    """
    A color used for elements needing less emphasis than `primary`.
    """
    on_primary_container: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `primary_container`.
    """
    secondary: OptionalColorValue = None
    """
    An accent color used for less prominent components in the UI, such as filter chips, 
    while expanding the opportunity for color expression.
    """
    on_secondary: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `secondary`.
    """
    secondary_container: OptionalColorValue = None
    """
    A color used for elements needing less emphasis than `secondary`.
    """
    on_secondary_container: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `secondary_container`.
    """
    tertiary: OptionalColorValue = None
    """
    A color used as a contrasting accent that can balance `primary` and `secondary` 
    colors or bring heightened attention to an element, such as an input field.
    """
    on_tertiary: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `tertiary`.
    """
    tertiary_container: OptionalColorValue = None
    """
    A color used for elements needing less emphasis than `tertiary`.
    """
    on_tertiary_container: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `tertiary_container`.
    """
    error: OptionalColorValue = None
    """
    The color to use for input validation errors, e.g. for `TextField.error_text`.
    """
    on_error: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `error`.
    """
    error_container: OptionalColorValue = None
    """
    A color used for error elements needing less emphasis than `error`.
    """
    on_error_container: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `error_container`.
    """
    background: OptionalColorValue = None
    """
    A color that typically appears behind scrollable content.
    """
    on_background: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `background`.
    """
    surface: OptionalColorValue = None
    """
    The background color for widgets like `Card`.
    """
    on_surface: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `surface`.
    """
    surface_variant: OptionalColorValue = None
    """
    A color variant of `surface` that can be used for differentiation against a 
    component using `surface`.
    """
    on_surface_variant: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `surface_variant`.
    """
    outline: OptionalColorValue = None
    """
    A utility color that creates boundaries and emphasis to improve usability.
    """
    outline_variant: OptionalColorValue = None
    """
    A utility color that creates boundaries for decorative elements when a 3:1 contrast 
    isn’t required, such as for dividers or decorative elements.
    """
    shadow: OptionalColorValue = None
    """
    A color use to paint the drop shadows of elevated components.
    """
    scrim: OptionalColorValue = None
    """
    A color use to paint the scrim around of modal components.
    """
    inverse_surface: OptionalColorValue = None
    """
    A surface color used for displaying the reverse of what’s seen in the surrounding 
    UI, for example in a `SnackBar` to bring attention to an alert.
    """
    on_inverse_surface: OptionalColorValue = None
    """
    A color that's clearly legible when drawn on `inverse_surface`.
    """
    inverse_primary: OptionalColorValue = None
    """
    An accent color used for displaying a highlight color on `inverse_surface` 
    backgrounds, like button text in a `SnackBar`.
    """
    surface_tint: OptionalColorValue = None
    """
    A color used as an overlay on a surface color to indicate a component's elevation.
    """
    on_primary_fixed: OptionalColorValue = None
    """
    A color that is used for text and icons that exist on top of elements having 
    `primary_fixed` color.
    """
    on_secondary_fixed: OptionalColorValue = None
    """
    A color that is used for text and icons that exist on top of elements having 
    `secondary_fixed` color.
    """
    on_tertiary_fixed: OptionalColorValue = None
    """
    A color that is used for text and icons that exist on top of elements having 
    `tertiary_fixed` color.
    """
    on_primary_fixed_variant: OptionalColorValue = None
    """
    A color that provides a lower-emphasis option for text and icons than 
    `on_primary_fixed`.
    """
    on_secondary_fixed_variant: OptionalColorValue = None
    """
    A color that provides a lower-emphasis option for text and icons than 
    `on_secondary_fixed`.
    """
    on_tertiary_fixed_variant: OptionalColorValue = None
    """
    A color that provides a lower-emphasis option for text and icons than 
    `on_tertiary_fixed`.
    """
    primary_fixed: OptionalColorValue = None
    """
    A substitute for `primary_container` that's the same color for the dark and light 
    themes.
    """
    secondary_fixed: OptionalColorValue = None
    """
    A substitute for `secondary_container` that's the same color for the dark and light 
    themes.
    """
    tertiary_fixed: OptionalColorValue = None
    """
    A substitute for `tertiary_container` that's the same color for dark and light 
    themes.
    """
    primary_fixed_dim: OptionalColorValue = None
    """
    A color used for elements needing more emphasis than `primary_fixed`.
    """
    secondary_fixed_dim: OptionalColorValue = None
    """
    A color used for elements needing more emphasis than `secondary_fixed`.
    """
    surface_bright: OptionalColorValue = None
    """
    A color that's always the lightest in the dark or light theme.
    """
    surface_container: OptionalColorValue = None
    surface_container_high: OptionalColorValue = None
    surface_container_low: OptionalColorValue = None
    surface_container_lowest: OptionalColorValue = None
    surface_dim: OptionalColorValue = None
    tertiary_fixed_dim: OptionalColorValue = None


@dataclass
class TextTheme:
    body_large: OptionalTextStyle = None
    body_medium: OptionalTextStyle = None
    body_small: OptionalTextStyle = None
    display_large: OptionalTextStyle = None
    display_medium: OptionalTextStyle = None
    display_small: OptionalTextStyle = None
    headline_large: OptionalTextStyle = None
    headline_medium: OptionalTextStyle = None
    headline_small: OptionalTextStyle = None
    label_large: OptionalTextStyle = None
    label_medium: OptionalTextStyle = None
    label_small: OptionalTextStyle = None
    title_large: OptionalTextStyle = None
    title_medium: OptionalTextStyle = None
    title_small: OptionalTextStyle = None


@dataclass
class ScrollbarTheme:
    thumb_visibility: Optional[ControlStateValue[bool]] = None
    thickness: Optional[ControlStateValue[OptionalNumber]] = None
    track_visibility: Optional[ControlStateValue[bool]] = None
    radius: OptionalNumber = None
    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    track_color: Optional[ControlStateValue[ColorValue]] = None
    track_border_color: Optional[ControlStateValue[ColorValue]] = None
    cross_axis_margin: OptionalNumber = None
    main_axis_margin: OptionalNumber = None
    min_thumb_length: OptionalNumber = None
    interactive: OptionalBool = None


@dataclass
class TabsTheme:
    divider_color: OptionalColorValue = None
    indicator_border_radius: OptionalBorderRadiusValue = None
    indicator_border_side: OptionalBorderSide = None
    indicator_padding: OptionalPaddingValue = None
    indicator_color: OptionalColorValue = None
    indicator_tab_size: OptionalBool = None
    label_color: OptionalColorValue = None
    unselected_label_color: OptionalColorValue = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    label_padding: OptionalPaddingValue = None
    label_text_style: OptionalTextStyle = None
    unselected_label_text_style: OptionalTextStyle = None


@dataclass
class SystemOverlayStyle:
    status_bar_color: OptionalColorValue = None
    system_navigation_bar_color: OptionalColorValue = None
    system_navigation_bar_divider_color: OptionalColorValue = None
    enforce_system_navigation_bar_contrast: OptionalBool = None
    enforce_system_status_bar_contrast: OptionalBool = None
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
    title_text_style: OptionalTextStyle = None
    content_text_style: OptionalTextStyle = None
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
    enable_feedback: OptionalBool = None
    disabled_mouse_cursor: Optional[MouseCursor] = None
    enabled_mouse_cursor: Optional[MouseCursor] = None
    shape: Optional[OutlinedBorder] = None
    text_style: OptionalTextStyle = None
    visual_density: Optional[VisualDensity] = None
    border_side: OptionalBorderSide = None
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
    enable_feedback: OptionalBool = None
    disabled_mouse_cursor: Optional[MouseCursor] = None
    enabled_mouse_cursor: Optional[MouseCursor] = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Optional[VisualDensity] = None
    border_side: OptionalBorderSide = None
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
    show_drag_handle: OptionalBool = None
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
    color: Optional[ControlStateValue[ColorValue]] = None
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
    label_text_style: OptionalTextStyle = None
    secondary_label_text_style: OptionalTextStyle = None
    border_side: OptionalBorderSide = None
    brightness: Optional[Brightness] = None
    show_checkmark: OptionalBool = None
    avatar_constraints: Optional[BoxConstraints] = None
    delete_icon_size_constraints: Optional[BoxConstraints] = None


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
    enable_feedback: OptionalBool = None
    extended_padding: OptionalPaddingValue = None
    extended_text_style: OptionalTextStyle = None
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
    unselected_label_text_style: OptionalTextStyle = None
    selected_label_text_style: OptionalTextStyle = None
    label_type: Optional[NavigationRailLabelType] = None
    min_width: OptionalNumber = None
    min_extended_width: OptionalNumber = None
    group_alignment: OptionalNumber = None
    use_indicator: OptionalBool = None


@dataclass
class AppBarTheme:
    """
    Customizes the appearance of https://flet.dev/docs/controls/appbar across the app.
    """

    color: OptionalColorValue = None
    """
    Overrides the default value of `AppBar.color` in all descendant `AppBar` controls.
    """

    bgcolor: OptionalColorValue = None
    """
    Overrides the default value of `AppBar.bgcolor` in all descendant `AppBar` controls.
    """

    shadow_color: OptionalColorValue = None
    """
    Overrides the default value of `AppBar.shadow_color` in all descendant `AppBar`
    controls.
    """

    surface_tint_color: OptionalColorValue = None
    """
    Overrides the default value of `AppBar.surface_tint_color` in all descendant
    `AppBar` controls.
    """

    foreground_color: OptionalColorValue = None
    """
    TBD
    """

    elevation: OptionalNumber = None
    """
    Overrides the default value of `AppBar.elevation` in all descendant `AppBar`
    controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of `AppBar.shape` in all descendant `AppBar` controls.
    """

    title_text_style: OptionalTextStyle = None
    """
    Overrides the default value of `AppBar.title_text_style` in all descendant
    `AppBar` controls.
    """

    toolbar_text_style: OptionalTextStyle = None
    """
    Overrides the default value of `AppBar.toolbar_text_style` in all descendant
    `AppBar` controls.
    """

    center_title: OptionalBool = None
    """
    Overrides the default value of `AppBar.center_title` in all descendant `AppBar`
    controls.
    """

    title_spacing: OptionalNumber = None
    """
    Overrides the default value of `AppBar.title_spacing` in all descendant `AppBar`
    controls.
    """

    scroll_elevation: OptionalNumber = None
    """
    Overrides the default value of `AppBar.scroll_elevation` in all descendant
    `AppBar` controls.
    """

    toolbar_height: OptionalNumber = None
    """
    Overrides the default value of `AppBar.toolbar_height` in all descendant `AppBar`
    controls.
    """

    actions_padding: OptionalPaddingValue = None
    """
    TBD
    """


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
    fill_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    splash_radius: OptionalNumber = None
    height: OptionalNumber = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class CheckboxTheme:
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    check_color: Optional[ControlStateValue[ColorValue]] = None
    fill_color: Optional[ControlStateValue[ColorValue]] = None
    splash_radius: OptionalNumber = None
    border_side: OptionalBorderSide = None
    visual_density: Optional[VisualDensity] = None
    shape: Optional[OutlinedBorder] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class BadgeTheme:
    bgcolor: OptionalColorValue = None
    text_color: OptionalColorValue = None
    small_size: OptionalNumber = None
    large_size: OptionalNumber = None
    alignment: Optional[Alignment] = None
    padding: OptionalPaddingValue = None
    offset: Optional[OffsetValue] = None
    text_style: OptionalTextStyle = None


@dataclass
class SwitchTheme:
    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    track_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    thumb_icon: Optional[ControlStateValue[str]] = None
    track_outline_width: Optional[ControlStateValue[OptionalNumber]] = None
    splash_radius: OptionalNumber = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    padding: OptionalPaddingValue = None


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
    content_text_style: OptionalTextStyle = None
    width: OptionalNumber = None
    alignment: Optional[Alignment] = None
    show_close_icon: OptionalBool = None
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
    content_text_style: OptionalTextStyle = None


@dataclass
class DatePickerTheme:
    bgcolor: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    divider_color: OptionalColorValue = None
    header_bgcolor: OptionalColorValue = None
    today_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    day_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    day_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    day_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: OptionalNumber = None
    range_picker_elevation: OptionalNumber = None
    day_text_style: OptionalTextStyle = None
    weekday_text_style: OptionalTextStyle = None
    year_text_style: OptionalTextStyle = None
    shape: Optional[OutlinedBorder] = None
    cancel_button_style: Optional[ButtonStyle] = None
    confirm_button_style: Optional[ButtonStyle] = None
    header_foreground_color: OptionalColorValue = None
    header_headline_text_style: OptionalTextStyle = None
    header_help_text_style: OptionalTextStyle = None
    range_picker_bgcolor: OptionalColorValue = None
    range_picker_header_bgcolor: OptionalColorValue = None
    range_picker_header_foreground_color: OptionalColorValue = None
    today_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    range_picker_shape: Optional[OutlinedBorder] = None
    range_picker_header_help_text_style: OptionalTextStyle = None
    range_picker_header_headline_text_style: OptionalTextStyle = None
    range_picker_surface_tint_color: OptionalColorValue = None
    range_selection_bgcolor: OptionalColorValue = None
    range_selection_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    today_border_side: OptionalBorderSide = None
    year_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    year_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    year_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    day_shape: Optional[ControlStateValue[OutlinedBorder]] = None
    locale: Optional[Locale] = None


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
    day_period_text_style: OptionalTextStyle = None
    dial_text_style: OptionalTextStyle = None
    help_text_style: OptionalTextStyle = None
    hour_minute_text_style: OptionalTextStyle = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    day_period_shape: Optional[OutlinedBorder] = None
    hour_minute_shape: Optional[OutlinedBorder] = None
    day_period_border_side: OptionalBorderSide = None
    padding: OptionalPaddingValue = None
    time_selector_separator_color: Optional[ControlStateValue[ColorValue]] = None
    time_selector_separator_text_style: Optional[ControlStateValue[TextStyle]] = None


@dataclass
class DropdownMenuTheme:
    menu_style: Optional[MenuStyle] = None
    text_style: OptionalTextStyle = None


@dataclass
class ListTileTheme:
    icon_color: OptionalColorValue = None
    text_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    selected_tile_color: OptionalColorValue = None
    selected_color: OptionalColorValue = None
    is_three_line: OptionalBool = None
    enable_feedback: OptionalBool = None
    dense: OptionalBool = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Optional[VisualDensity] = None
    content_padding: OptionalPaddingValue = None
    min_vertical_padding: OptionalPaddingValue = None
    horizontal_spacing: OptionalNumber = None
    min_leading_width: OptionalNumber = None
    title_text_style: OptionalTextStyle = None
    subtitle_text_style: OptionalTextStyle = None
    leading_and_trailing_text_style: OptionalTextStyle = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    min_tile_height: OptionalNumber = None


@dataclass
class TooltipTheme:
    height: OptionalNumber = None
    text_style: OptionalTextStyle = None
    enable_feedback: OptionalBool = None
    exclude_from_semantics: OptionalBool = None
    prefer_below: OptionalBool = None
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
    value_indicator_text_style: OptionalTextStyle = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
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
    thumb_size: Optional[ControlStateValue[Size]] = None
    year_2023: OptionalBool = None


@dataclass
class ProgressIndicatorTheme:
    color: OptionalColorValue = None
    circular_track_color: OptionalColorValue = None
    linear_track_color: OptionalColorValue = None
    refresh_bgcolor: OptionalColorValue = None
    linear_min_height: OptionalNumber = None
    border_radius: OptionalBorderRadiusValue = None
    track_gap: OptionalNumber = None
    circular_track_padding: OptionalPaddingValue = None
    size_constraints: Optional[BoxConstraints] = None
    stop_indicator_color: OptionalColorValue = None
    stop_indicator_radius: OptionalNumber = None
    stroke_align: OptionalNumber = None
    stroke_cap: Optional[StrokeCap] = None
    stroke_width: OptionalNumber = None
    year_2023: OptionalBool = None


@dataclass
class PopupMenuTheme:
    color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    text_style: OptionalTextStyle = None
    label_text_style: OptionalTextStyle = None
    enable_feedback: OptionalBool = None
    elevation: OptionalNumber = None
    icon_size: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    menu_position: Optional[PopupMenuPosition] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    menu_padding: OptionalPaddingValue = None


@dataclass
class SearchBarTheme:
    bgcolor: OptionalColorValue = None
    text_capitalization: Optional[TextCapitalization] = None
    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    surface_tint_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[ControlStateValue[OptionalNumber]] = None
    text_style: Optional[ControlStateValue[TextStyle]] = None
    hint_style: Optional[ControlStateValue[TextStyle]] = None
    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    padding: Optional[ControlStateValue[PaddingValue]] = None
    size_constraints: Optional[BoxConstraints] = None
    border_side: Optional[ControlStateValue[BorderSide]] = None


@dataclass
class SearchViewTheme:
    bgcolor: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    divider_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    header_hint_text_style: OptionalTextStyle = None
    header_text_style: OptionalTextStyle = None
    shape: Optional[OutlinedBorder] = None
    border_side: OptionalBorderSide = None
    size_constraints: Optional[BoxConstraints] = None
    header_height: OptionalNumber = None
    padding: OptionalPaddingValue = None
    bar_padding: OptionalPaddingValue = None
    shrink_wrap: OptionalBool = None


@dataclass
class NavigationDrawerTheme:
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    tile_height: OptionalNumber = None
    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    indicator_shape: Optional[OutlinedBorder] = None
    indicator_size: Optional[Size] = None


@dataclass
class NavigationBarTheme:
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: OptionalNumber = None
    height: OptionalNumber = None
    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    indicator_shape: Optional[OutlinedBorder] = None
    label_behavior: Optional[NavigationBarLabelBehavior] = None
    label_padding: OptionalPaddingValue = None


@dataclass
class SegmentedButtonTheme:
    selected_icon: Optional[IconValue] = None
    style: Optional[ButtonStyle] = None


@dataclass
class IconTheme:
    color: OptionalColorValue = None
    apply_text_scaling: OptionalBool = None
    fill: OptionalNumber = None
    opacity: OptionalNumber = None
    size: OptionalNumber = None
    optical_size: OptionalNumber = None
    grade: OptionalNumber = None
    weight: OptionalNumber = None
    shadows: Optional[list[BoxShadow]] = None


@dataclass
class DataTableTheme:
    checkbox_horizontal_margin: OptionalNumber = None
    column_spacing: OptionalNumber = None
    data_row_max_height: OptionalNumber = None
    data_row_min_height: OptionalNumber = None
    data_row_color: Optional[ControlStateValue[ColorValue]] = None
    data_text_style: OptionalTextStyle = None
    divider_thickness: OptionalNumber = None
    horizontal_margin: OptionalNumber = None
    heading_text_style: OptionalTextStyle = None
    heading_row_color: Optional[ControlStateValue[ColorValue]] = None
    heading_row_height: OptionalNumber = None
    data_row_cursor: Optional[ControlStateValue[MouseCursor]] = None
    decoration: Optional[BoxDecoration] = None
    heading_row_alignment: Optional[MainAxisAlignment] = None
    heading_cell_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class Theme:
    color_scheme_seed: OptionalColorValue = None
    primary_swatch: OptionalColorValue = None
    font_family: Optional[str] = None
    use_material3: OptionalBool = None
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
