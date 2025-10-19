from dataclasses import dataclass, field
from enum import Enum, IntFlag
from typing import TYPE_CHECKING, Optional

import flet as ft
from flet.controls.animation import AnimationCurve

if TYPE_CHECKING:
    from flet_map.map import Map  # noqa

__all__ = [
    "AttributionAlignment",
    "Camera",
    "CameraFit",
    "CursorKeyboardRotationConfiguration",
    "CursorRotationBehaviour",
    "DashedStrokePattern",
    "DottedStrokePattern",
    "FadeInTileDisplay",
    "InstantaneousTileDisplay",
    "InteractionConfiguration",
    "InteractionFlag",
    "KeyboardConfiguration",
    "MapEvent",
    "MapEventSource",
    "MapHoverEvent",
    "MapLatitudeLongitude",
    "MapLatitudeLongitudeBounds",
    "MapPointerEvent",
    "MapPositionChangeEvent",
    "MapTapEvent",
    "MultiFingerGesture",
    "PatternFit",
    "SolidStrokePattern",
    "StrokePattern",
    "TileDisplay",
    "TileLayerEvictErrorTileStrategy",
]


class TileLayerEvictErrorTileStrategy(Enum):
    """Strategies on how to handle tile errors."""

    NONE = "none"
    """Never evict images for tiles which failed to load."""

    DISPOSE = "dispose"
    """Evict images for tiles which failed to load when they are pruned."""

    NOT_VISIBLE = "notVisible"
    """
    Evict images for tiles which failed to load and:
        - do not belong to the current zoom level AND/OR
        - are not visible
    """

    NOT_VISIBLE_RESPECT_MARGIN = "notVisibleRespectMargin"
    """
    Evict images for tiles which failed to load and:
        - do not belong to the current zoom level AND/OR
        - are not visible, respecting the pruning buffer
            (the maximum of the `keep_buffer` and `pan_buffer`).
    """


class AttributionAlignment(Enum):
    """Position to anchor [`RichAttribution`][(p).] control relative to the map."""

    BOTTOM_LEFT = "bottomLeft"
    """The bottom left corner."""

    BOTTOM_RIGHT = "bottomRight"
    """The bottom right corner."""


class PatternFit(Enum):
    """
    Determines how a non-solid [`StrokePattern`][(p).] should be fit to a line
    when their lengths are not equal or multiples
    """

    NONE = "none"
    """
    Don't apply any specific fit to the pattern - repeat exactly as specified,
    and stop when the last point is reached.

    Not recommended, as it may leave a gap between the final segment and the last
    point, making it unclear where the line ends.
    """

    SCALE_DOWN = "scaleDown"
    """
    Scale the pattern to ensure it fits an integer number of times into the
    polyline (smaller version regarding rounding, cf. [`SCALE_UP`][(c).]).
    """

    SCALE_UP = "scaleUp"
    """
    Scale the pattern to ensure it fits an integer number of times into the
    polyline (bigger version regarding rounding, cf. [`SCALE_DOWN`][(c).]).
    """

    APPEND_DOT = "appendDot"
    """
    Uses the pattern exactly, truncating the final dash if it does not fit, or
    adding a single dot at the last point if the final dash does not reach the
    last point (there is a gap at that location).
    """

    EXTEND_FINAL_DASH = "extendFinalDash"
    """
    Uses the pattern exactly, truncating the final dash if it does not fit, or
    extending the final dash to the last point if it would not normally reach
    that point (there is a gap at that location).

    Only useful when working with [`DashedStrokePattern`][(p).].
    Similar to `APPEND_DOT` for `DottedStrokePattern`.
    """


@dataclass
class Camera:
    center: "MapLatitudeLongitude"
    """
    The center of this camera.
    """

    zoom: ft.Number
    """
    Defines how far this camera is zoomed.
    """

    min_zoom: ft.Number
    """
    The minimum allowed zoom level.
    """

    max_zoom: ft.Number
    """
    The maximum allowed zoom level.
    """

    rotation: ft.Number
    """
    The rotation (in degrees) of the camera.
    """


@dataclass
class StrokePattern:
    """
    Determines whether a stroke should be solid, dotted, or dashed,
    and the exact characteristics of each.

    This is an abstract class and shouldn't be used directly.

    See usable derivatives:
    - [`SolidStrokePattern`][(p).]
    - [`DashedStrokePattern`][(p).]
    - [`DottedStrokePattern`][(p).]
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class SolidStrokePattern(StrokePattern):
    """A solid/unbroken stroke pattern."""

    def __post_init__(self):
        self._type = "solid"


@dataclass
class DashedStrokePattern(StrokePattern):
    """
    A stroke pattern of alternating dashes and gaps, defined by [`segments`][(c).].

    Raises:
        ValueError: If [`segments`][(c).] does not contain at least two items,
            or has an odd length.
    """

    segments: list[ft.Number] = field(default_factory=list)
    """
    A list of alternating dash and gap lengths, in pixels.

    Raises:
        ValueError: If the list does not contain at least two items,
            or if its length is not even.
    """

    pattern_fit: PatternFit = PatternFit.SCALE_UP
    """
    Determines how this stroke pattern should be fit to a line when their lengths
    are not equal or multiples.
    """

    def __post_init__(self):
        if len(self.segments) < 2:
            raise ValueError(
                f"segments must contain at least two items, got {len(self.segments)}"
            )
        if len(self.segments) % 2 != 0:
            raise ValueError("segments must have an even length")
        self._type = "dashed"


@dataclass
class DottedStrokePattern(StrokePattern):
    """
    A stroke pattern of circular dots, spaced with [`spacing_factor`][(c).].
    """

    spacing_factor: ft.Number = 1.5
    """
    The multiplier used to calculate the spacing between dots in a dotted polyline,
    with respect to `Polyline.stroke_width` / `Polygon.border_stroke_width`.
    A value of `1.0` will result in spacing equal to the `stroke_width`.
    Increasing the value increases the spacing with the same scaling.

    May also be scaled by the use of [`PatternFit.SCALE_UP`][(p).].

    Raises:
        ValueError: If it is less than or equal to zero.
    """

    pattern_fit: PatternFit = PatternFit.SCALE_UP
    """
    Determines how this stroke pattern should be fit to a line when their
    lengths are not equal or multiples.
    """

    def __post_init__(self):
        if self.spacing_factor <= 0:
            raise ValueError(
                f"spacing_factor must be greater than to 0.0, got {self.spacing_factor}"
            )
        self._type = "dotted"


@dataclass
class MapLatitudeLongitude:
    """Map coordinates in degrees."""

    latitude: ft.Number
    """The latitude point of this coordinate."""

    longitude: ft.Number
    """The longitude point of this coordinate."""


@dataclass
class MapLatitudeLongitudeBounds:
    """
    Both corners have to be on opposite sites, but it doesn't matter
    which opposite corners or in what order the corners are provided.
    """

    corner_1: MapLatitudeLongitude
    """The corner 1."""

    corner_2: MapLatitudeLongitude
    """The corner 2."""


class InteractionFlag(IntFlag):
    """
    Flags to enable/disable certain interaction events on the map.

    Example:
        - [`InteractionFlag.ALL`][(p).] to enable all events
        - [`InteractionFlag.NONE`][(p).] to disable all events
    """

    NONE = 0
    """No interaction."""

    DRAG = 1 << 0
    """Panning with a single finger or cursor."""

    FLING_ANIMATION = 1 << 1
    """Fling animation after panning if velocity is great enough."""

    PINCH_MOVE = 1 << 2
    """Panning with multiple fingers."""

    PINCH_ZOOM = 1 << 3
    """Zooming with a multi-finger pinch gesture."""

    DOUBLE_TAP_ZOOM = 1 << 4
    """Zooming with a single-finger double tap gesture."""

    DOUBLE_TAP_DRAG_ZOOM = 1 << 5
    """Zooming with a single-finger double-tap-drag gesture."""

    SCROLL_WHEEL_ZOOM = 1 << 6
    """Zooming with a mouse scroll wheel."""

    ROTATE = 1 << 7
    """Rotation with two-finger twist gesture."""

    ALL = (
        (1 << 0)
        | (1 << 1)
        | (1 << 2)
        | (1 << 3)
        | (1 << 4)
        | (1 << 5)
        | (1 << 6)
        | (1 << 7)
    )
    """All available interactive flags."""

    @staticmethod
    def has_flag(left_flags: int, right_flags: int) -> bool:
        """
        Returns:
            `True` if `left_flags` has at least one member
                in `right_flags` (intersection).
        """
        return left_flags & right_flags != 0

    @staticmethod
    def has_multi_finger(flags: int) -> bool:
        """
        Returns:
            `True` if any multi-finger gesture flags
                ([`MultiFingerGesture.PINCH_MOVE`][(p).],
                [`MultiFingerGesture.PINCH_ZOOM`][(p).],
                [`MultiFingerGesture.ROTATE`][(p).]) are enabled.
        """
        return InteractionFlag.has_flag(
            flags,
            (
                MultiFingerGesture.PINCH_MOVE
                | MultiFingerGesture.PINCH_ZOOM
                | MultiFingerGesture.ROTATE
            ),
        )

    @staticmethod
    def has_drag(flags: int) -> bool:
        """
        Returns:
            `True` if the [`DRAG`][flet_map.InteractionFlag.DRAG] interaction
                flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.DRAG)

    @staticmethod
    def has_fling_animation(flags: int) -> bool:
        """
        Returns:
            `True` if the [`FLING_ANIMATION`][flet_map.InteractionFlag.FLING_ANIMATION]
                interaction flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.FLING_ANIMATION)

    @staticmethod
    def has_pinch_move(flags: int) -> bool:
        """
        Returns:
            `True` if the [`PINCH_MOVE`][flet_map.InteractionFlag.PINCH_MOVE]
                interaction flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.PINCH_MOVE)

    @staticmethod
    def has_fling_pinch_zoom(flags: int) -> bool:
        """
        Returns:
            `True` if the [`PINCH_ZOOM`][flet_map.InteractionFlag.PINCH_ZOOM]
                interaction flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.PINCH_ZOOM)

    @staticmethod
    def has_double_tap_drag_zoom(flags: int) -> bool:
        """
        Returns:
            `True` if the
                [`DOUBLE_TAP_DRAG_ZOOM`][flet_map.InteractionFlag.DOUBLE_TAP_DRAG_ZOOM]
                interaction flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.DOUBLE_TAP_DRAG_ZOOM)

    @staticmethod
    def has_double_tap_zoom(flags: int) -> bool:
        """
        Returns:
            `True` if the [`DOUBLE_TAP_ZOOM`][flet_map.InteractionFlag.DOUBLE_TAP_ZOOM]
                interaction flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.DOUBLE_TAP_ZOOM)

    @staticmethod
    def has_rotate(flags: int) -> bool:
        """
        Returns:
            `True` if the [`ROTATE`][(c).] interactive flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.ROTATE)

    @staticmethod
    def has_scroll_wheel_zoom(flags: int) -> bool:
        """
        Returns:
            `True` if the [`SCROLL_WHEEL_ZOOM`][(c).] interaction flag is enabled.
        """
        return InteractionFlag.has_flag(flags, InteractionFlag.SCROLL_WHEEL_ZOOM)


class MultiFingerGesture(IntFlag):
    """Flags to enable/disable certain multi-finger gestures on the map."""

    NONE = 0
    """No multi-finger gesture."""

    PINCH_MOVE = 1 << 0
    """Pinch move gesture, which allows moving the map by dragging with two fingers."""

    PINCH_ZOOM = 1 << 1
    """
    Pinch zoom gesture, which allows zooming in and out by pinching with two fingers.
    """

    ROTATE = 1 << 2
    """Rotate gesture, which allows rotating the map by twisting two fingers."""

    ALL = (1 << 0) | (1 << 1) | (1 << 2)
    """All multi-finger gestures defined in this enum."""


@dataclass
class InteractionConfiguration:
    enable_multi_finger_gesture_race: bool = False
    """
    If `True`, then [`rotation_threshold`][(c).] and [`pinch_zoom_threshold`][(c).]
    and [`pinch_move_threshold`][(c).] will race.
    If multiple gestures win at the same time, then precedence:
    [`pinch_zoom_win_gestures`][(c).] > [`rotation_win_gestures`][(c).] >
    [`pinch_move_win_gestures`][(c).]
    """

    pinch_move_threshold: ft.Number = 40.0
    """
    Map starts to move when `pinch_move_threshold` has been achieved
    or another multi finger gesture wins which allows
    [`MultiFingerGesture.PINCH_MOVE`][(p).].

    Note:
        If [`InteractionConfiguration.flags`][(p).] doesn't contain
        [`InteractionFlag.PINCH_MOVE`][(p).] or
        [`enable_multi_finger_gesture_race`][(c).] is false then pinch move cannot win.
    """

    scroll_wheel_velocity: ft.Number = 0.005
    """
    The used velocity how fast the map should zoom in or out by scrolling
    with the scroll wheel of a mouse.
    """

    pinch_zoom_threshold: ft.Number = 0.5
    """
    Map starts to zoom when `pinch_zoom_threshold` has been achieved or
    another multi finger gesture wins which allows
    [`MultiFingerGesture.PINCH_ZOOM`][(p).].

    Note:
        If [`InteractionConfiguration.flags`][(p).]
        doesn't contain [`InteractionFlag.PINCH_ZOOM`][(p).]
        or [`enable_multi_finger_gesture_race`][(c).] is false then zoom cannot win.
    """

    rotation_threshold: ft.Number = 20.0
    """
    Map starts to rotate when `rotation_threshold` has been achieved or
    another multi finger gesture wins which allows [`MultiFingerGesture.ROTATE`][(p).].

    Note:
        If [`InteractionConfiguration.flags`][(p).]
        doesn't contain [`InteractionFlag.ROTATE`][(p).]
        or [`enable_multi_finger_gesture_race`][(c).] is false then rotate cannot win.
    """

    flags: InteractionFlag = InteractionFlag.ALL
    """
    Defines the map events to be enabled/disabled.
    """

    rotation_win_gestures: MultiFingerGesture = MultiFingerGesture.ROTATE
    """
    When [`rotation_threshold`][(c).] wins over [`pinch_zoom_threshold`][(c).] and
    [`pinch_move_threshold`][(c).] then `rotation_win_gestures` gestures will be used.
    """

    pinch_move_win_gestures: MultiFingerGesture = (
        MultiFingerGesture.PINCH_ZOOM | MultiFingerGesture.PINCH_MOVE
    )
    """
    When [`pinch_move_threshold`][(c).] wins over [`rotation_threshold`][(c).]
    and [`pinch_zoom_threshold`][(c).] then `pinch_move_win_gestures` gestures
    will be used.

    By default [`MultiFingerGesture.PINCH_MOVE`][(p).]
    and [`MultiFingerGesture.PINCH_ZOOM`][(p).]
    gestures will take effect see [`MultiFingerGesture`][(p).] for custom settings.
    """

    pinch_zoom_win_gestures: MultiFingerGesture = (
        MultiFingerGesture.PINCH_ZOOM | MultiFingerGesture.PINCH_MOVE
    )
    """
    When [`pinch_zoom_threshold`][(c).] wins over [`rotation_threshold`][(c).]
    and [`pinch_move_threshold`][(c).]
    then `pinch_zoom_win_gestures` gestures will be used.

    By default [`MultiFingerGesture.PINCH_ZOOM`][(p).]
    and [`MultiFingerGesture.PINCH_MOVE`][(p).]
    gestures will take effect see `MultiFingerGesture` for custom settings.
    """

    keyboard_configuration: "KeyboardConfiguration" = field(
        default_factory=lambda: KeyboardConfiguration()
    )
    """
    Options to configure how keyboard keys may be used to control the map.

    Keyboard movements using the arrow keys are enabled by default.
    """

    cursor_keyboard_rotation_configuration: "CursorKeyboardRotationConfiguration" = (
        field(default_factory=lambda: CursorKeyboardRotationConfiguration())
    )
    """
    Options to control the keyboard and mouse cursor being used together
    to rotate the map.
    """


class MapEventSource(Enum):
    """Defines the source of a [`MapEvent`][(p).]."""

    MAP_CONTROLLER = "mapController"
    """The `MapEvent` is caused programmatically by the `MapController`."""

    TAP = "tap"
    """The `MapEvent` is caused by a tap gesture."""

    SECONDARY_TAP = "secondaryTap"
    """The `MapEvent` is caused by a secondary tap gesture."""

    LONG_PRESS = "longPress"
    """The `MapEvent` is caused by a long press gesture."""

    DOUBLE_TAP = "doubleTap"
    """The `MapEvent` is caused by a double tap gesture."""

    DOUBLE_TAP_HOLD = "doubleTapHold"
    """The `MapEvent` is caused by a double tap and hold gesture."""

    DRAG_START = "dragStart"
    """The `MapEvent` is caused by the start of a drag gesture."""

    ON_DRAG = "onDrag"
    """The `MapEvent` is caused by a drag update gesture."""

    DRAG_END = "dragEnd"
    """The `MapEvent` is caused by the end of a drag gesture."""

    MULTI_FINGER_GESTURE_START = "multiFingerGestureStart"
    """The `MapEvent` is caused by the start of a two finger gesture."""

    ON_MULTI_FINGER = "onMultiFinger"
    """The `MapEvent` is caused by a two finger gesture update."""

    MULTI_FINGER_GESTURE_END = "multiFingerEnd"
    """The `MapEvent` is caused by a the end of a two finger gesture."""

    FLING_ANIMATION_CONTROLLER = "flingAnimationController"
    """
    The `MapEvent` is caused by the `AnimationController` while
    performing the fling gesture.
    """

    DOUBLE_TAP_ZOOM_ANIMATION_CONTROLLER = "doubleTapZoomAnimationController"
    """
    The `MapEvent` is caused by the `AnimationController`
    while performing the double tap zoom in animation.
    """

    INTERACTIVE_FLAGS_CHANGED = "InteractionFlagsChanged"
    """The `MapEvent` is caused by a change of the interactive flags."""

    FIT_CAMERA = "fitCamera"
    """The `MapEvent` is caused by calling fit_camera."""

    CUSTOM = "custom"
    """The `MapEvent` is caused by a custom source."""

    SCROLL_WHEEL = "scrollWheel"
    """The `MapEvent` is caused by a scroll wheel zoom gesture."""

    NON_ROTATED_SIZE_CHANGE = "nonRotatedSizeChange"
    """The `MapEvent` is caused by a size change of the `Map` constraints."""

    CURSOR_KEYBOARD_ROTATION = "cursorKeyboardRotation"
    """The `MapEvent` is caused by a 'CTRL + drag' rotation gesture."""

    KEYBOARD = "keyboard"
    """
    The `MapEvent` is caused by a keyboard key.
    See [`KeyboardConfiguration`][(p).] for details.
    """


@dataclass
class CameraFit:
    """
    Defines how the camera should fit the bounds or coordinates,
    depending on which one was provided.

    Raises:
        ValueError: If both [`bounds`][(c).] and [`coordinates`][(c).]
            are `None` or not `None`.
    """

    bounds: Optional[MapLatitudeLongitudeBounds] = None
    """
    The bounds which the camera should contain once it is fitted.

    Note:
        If this is not `None`, [`coordinates`][(c).] should be `None`, and vice versa.
    """

    coordinates: Optional[list[MapLatitudeLongitude]] = None
    """
    The coordinates which the camera should contain once it is fitted.

    Note:
        If this is not `None`, [`bounds`][(c).] should be `None`, and vice versa.
    """

    max_zoom: Optional[ft.Number] = None
    """
    The inclusive upper zoom limit used for the resulting fit.

    If the zoom level calculated for the fit exceeds the `max_zoom` value,
    `max_zoom` will be used instead.
    """

    min_zoom: ft.Number = 0.0
    """
    """

    padding: ft.PaddingValue = field(default_factory=lambda: ft.Padding.zero())
    """
    Adds a constant/pixel-based padding to the normal fit.
    """

    force_integer_zoom_level: bool = False
    """
    Whether the zoom level of the resulting fit should be rounded to the
    nearest integer level.
    """

    def __post_init__(self):
        if not (
            (self.bounds and not self.coordinates)
            or (self.coordinates and not self.bounds)
        ):
            raise ValueError(
                "only one of bounds or coordinates must be provided, not both"
            )


@dataclass
class MapTapEvent(ft.TapEvent["Map"]):
    coordinates: MapLatitudeLongitude
    """Coordinates of the point at which the tap occured."""


@dataclass
class MapHoverEvent(ft.HoverEvent["Map"]):
    coordinates: MapLatitudeLongitude


@dataclass
class MapPositionChangeEvent(ft.Event["Map"]):
    coordinates: MapLatitudeLongitude
    camera: Camera
    has_gesture: bool


@dataclass
class MapPointerEvent(ft.PointerEvent["Map"]):
    coordinates: MapLatitudeLongitude
    """Coordinates of the point at which the tap occured."""


@dataclass
class MapEvent(ft.Event["Map"]):
    source: MapEventSource
    """Who/what issued the event."""

    camera: Camera
    """The map camera after the event."""


@dataclass
class TileDisplay:
    """
    Defines how the tile should get displayed on the map.

    This is an abstract class and shouldn't be used directly.

    See usable derivatives:
    - `InstantaneousTileDisplay`
    - `FadeInTileDisplay`
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class InstantaneousTileDisplay(TileDisplay):
    """A `TileDisplay` that should get instantaneously displayed."""

    opacity: ft.Number = 1.0
    """
    The optional opacity of the tile.

    Raises:
        ValueError: If its value is not between `0.0` and `1.0` inclusive.
    """

    def __post_init__(self):
        if not (0.0 <= self.opacity <= 1.0):
            raise ValueError(
                f"opacity must be between 0.0 and 1.0 inclusive, got {self.opacity}"
            )
        self._type = "instantaneous"


@dataclass
class FadeInTileDisplay(TileDisplay):
    """A `TileDisplay` that should get faded in."""

    duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration(milliseconds=100)
    )
    """
    The duration of the fade in animation.
    """

    start_opacity: ft.Number = 0.0
    """
    Opacity start value when a tile is faded in.

    Raises:
        ValueError: If its value is not between `0.0` and `1.0` inclusive.
    """

    reload_start_opacity: ft.Number = 0.0
    """
    Opacity start value when a tile is reloaded.

    Raises:
        ValueError: If its value is not between `0.0` and `1.0` inclusive.
    """

    def __post_init__(self):
        if not (0.0 <= self.start_opacity <= 1.0):
            raise ValueError(
                "start_opacity must be between 0.0 and 1.0 inclusive, "
                f"got {self.start_opacity}"
            )
        if not (0.0 <= self.reload_start_opacity <= 1.0):
            raise ValueError(
                "reload_start_opacity must be between 0.0 and 1.0 inclusive, "
                f"got {self.reload_start_opacity}"
            )
        self._type = "fadein"


@dataclass
class KeyboardConfiguration:
    """
    Options to configure how keyboard keys may be used to control the map.
    When a key is pushed down, an animation starts, consisting of a curved
    portion which takes the animation to its maximum velocity, an indefinitely
    long animation at maximum velocity, then ended on the key up with another
    curved portion.

    If a key is pressed and released quickly, it might trigger a short animation
    called a 'leap'. The leap consists of a part of the curved portion, and also
    scales the velocity of the concerned gesture.

    Info:
        See [`CursorKeyboardRotationConfiguration`][(p).] for options
        to control the keyboard and
        mouse cursor being used together to rotate the map.
    """

    autofocus: bool = True
    """
    Whether to request focus as soon as the map control appears
    (and to enable keyboard controls).
    """

    animation_curve_duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration(milliseconds=450)
    )
    """
    Duration of the curved ([`AnimationCurve.EASE_IN`][flet.AnimationCurve.EASE_IN])
    portion of the animation occuring
    after a key down event (and after a key up event if
    [`animation_curve_reverse_duration`][(c).] is `None`)
    """

    animation_curve_reverse_duration: Optional[ft.DurationValue] = field(
        default_factory=lambda: ft.Duration(milliseconds=600)
    )
    """
    Duration of the curved (reverse
    [`AnimationCurve.EASE_IN`][flet.AnimationCurve.EASE_IN])
    portion of the animation occuring after a key up event.

    Set to `None` to use [`animation_curve_duration`][(c).].
    """

    animation_curve_curve: AnimationCurve = AnimationCurve.EASE_IN_OUT
    """
    Curve of the curved portion of the animation occuring after
    key down and key up events.
    """

    enable_arrow_keys_panning: bool = True
    """
    Whether to allow arrow keys to pan the map (in their respective directions).
    """

    enable_qe_rotating: bool = True
    """
    Whether to allow the `Q` & `E` keys (*) to rotate the map (`Q` rotates
    anticlockwise, `E` rotates clockwise).

    QE are only the physical and logical keys on QWERTY keyboards.
    On non- QWERTY keyboards, such as AZERTY,
    the keys in the same position as on the QWERTY keyboard is used (ie. AE on AZERTY).
    """

    enable_rf_zooming: bool = True
    """
    Whether to allow the `R` & `F` keys to zoom the map (`R` zooms IN
    (increases zoom level), `F` zooms OUT (decreases zoom level)).

    RF are only the physical and logical keys on QWERTY keyboards.
    On non- QWERTY keyboards, such as AZERTY,
    the keys in the same position as on the QWERTY keyboard is used (ie. RF on AZERTY).
    """

    enable_wasd_panning: bool = True
    """
    Whether to allow the `W`, `A`, `S`, `D` keys (*) to pan the map
    (in the directions UP, LEFT, DOWN, RIGHT respectively).

    WASD are only the physical and logical keys on QWERTY keyboards.
    On non- QWERTY keyboards, such as AZERTY,
    the keys in the same position as on the QWERTY keyboard is
    used (ie. ZQSD on AZERTY).

    If enabled, it is recommended to enable `enable_arrow_keys_panning`
    to provide panning functionality easily for left handed users.
    """

    leap_max_of_curve_component: ft.Number = 0.6
    """
    The percentage (0.0 - 1.0) of the curve animation component that is driven
    to (from 0), then in reverse from (to 0).

    Reducing means the leap occurs quicker (assuming a consistent curve
    animation duration). Also see `*_leap_velocity_multiplier` properties to
    change the distance of the leap assuming a consistent leap duration.

    For example, if set to 1, then the leap will take
    `animation_curve_duration + animation_curve_reverse_duration`
    to complete.

    Must be greater than 0 and less than or equal to 1.
    To disable leaping, or change the maximum length of the key press
    that will trigger a leap, see [`perform_leap_trigger_duration`][(c).].
    """

    max_rotate_velocity: ft.Number = 3
    """
    The maximum angular difference to apply per frame to the camera's rotation
    during a rotation animation.

    Measured in degrees. Negative numbers will flip the standard rotation keys.
    """

    max_zoom_velocity: ft.Number = 0.03
    """
    The maximum zoom level difference to apply per frame to the camera's zoom
    level during a zoom animation.

    Measured in zoom levels. Negative numbers will flip the standard zoom keys.
    """

    pan_leap_velocity_multiplier: ft.Number = 5
    """
    The amount to scale the panning offset velocity by during a leap animation.

    The larger the number, the larger the movement during a leap.
    To change the duration of a leap, see [`leap_max_of_curve_component`][(c).].
    """

    rotate_leap_velocity_multiplier: ft.Number = 3
    """
    The amount to scale the rotation velocity by during a leap animation

    The larger the number, the larger the rotation difference during a leap.
    To change the duration of a leap, see [`leap_max_of_curve_component`][(c).].

    This may cause the pan velocity to exceed [`max_rotate_velocity`][(c).].
    """

    zoom_leap_velocity_multiplier: ft.Number = 3
    """
    The amount to scale the zooming velocity by during a leap animation.

    The larger the number, the larger the zoom difference during a leap. To
    change the duration of a leap, see [`leap_max_of_curve_component`][(c).].

    This may cause the pan velocity to exceed [`max_zoom_velocity`][(c).].
    """

    perform_leap_trigger_duration: Optional[ft.DurationValue] = field(
        default_factory=lambda: ft.Duration(milliseconds=100)
    )
    """
    Maximum duration between the key down and key up events of an animation
    which will trigger a 'leap'.

    To customize the leap itself, see the [`leap_max_of_curve_component`][(c).] &
    `*leap_velocity_multiplier` ([`zoom_leap_velocity_multiplier`][(c).],
    [`pan_leap_velocity_multiplier`][(c).] and
    [`rotate_leap_velocity_multiplier`][(c).]) properties.

    Set to `None` to disable leaping.
    """

    @classmethod
    def disabled(cls) -> "KeyboardConfiguration":
        """
        Disable keyboard control of the map.

        Info:
            [`CursorKeyboardRotationConfiguration`][(p).] may still be active,
            and is not disabled if this is disabled.
        """
        return KeyboardConfiguration(
            enable_arrow_keys_panning=False,
            perform_leap_trigger_duration=None,
            autofocus=False,
        )


class CursorRotationBehaviour(Enum):
    """
    The behaviour of the cursor/keyboard rotation function in terms of the angle
    that the map is rotated to.

    Does not disable cursor/keyboard rotation, or adjust its triggers: see
    `CursorKeyboardRotationConfiguration.is_key_trriger`.
    """

    OFFSET = "offset"
    """
    Offset the current rotation of the map to the angle at which the
    user drags their cursor.
    """

    SET_NORTH = "setNorth"
    """
    Set the North of the map to the angle at which the user drags their cursor.
    """


@dataclass
class CursorKeyboardRotationConfiguration:
    """
    Options to configure cursor/keyboard rotation.

    Cursor/keyboard rotation is designed for desktop platforms,
    and allows the cursor to be used to set the rotation of the map
    whilst a keyboard key is held down (as triggered by `is_key_trriger`).
    """

    set_north_on_click: bool = True
    """
    Whether to set the North of the map to the clicked angle,
    when the user clicks their mouse without dragging
    (a `on_pointer_down` event followed by `on_pointer_up`
    without a change in rotation).
    """

    behavior: CursorRotationBehaviour = CursorRotationBehaviour.OFFSET
    """
    The behaviour of the cursor/keyboard rotation function in terms of the
    angle that the map is rotated to.

    Does not disable cursor/keyboard rotation, or
    adjust its triggers: see `is_key_trriger`.
    """

    # TODO
    trigger_keys: list = field(
        default_factory=lambda: [
            # ft.LogicalKeyboardKey.CONTROL,
            # ft.LogicalKeyboardKey.CONTROL_LEFT,
            # ft.LogicalKeyboardKey.CONTROL_RIGHT,
        ]
    )
    """
    List of keys that will trigger cursor/keyboard rotation, when pressed.
    """

    @classmethod
    def disabled(cls) -> "CursorKeyboardRotationConfiguration":
        """A disabled `CursorKeyboardRotationConfiguration`."""
        return CursorKeyboardRotationConfiguration(trigger_keys=[])
