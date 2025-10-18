from dataclasses import field
from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.types import (
    CameraFit,
    InteractionConfiguration,
    MapEvent,
    MapHoverEvent,
    MapLatitudeLongitude,
    MapPointerEvent,
    MapPositionChangeEvent,
    MapTapEvent,
)

__all__ = ["Map"]


@ft.control("Map")
class Map(ft.LayoutControl):
    """
    An interactive map that displays various layers.
    """

    layers: list[MapLayer]
    """
    A list of layers to be displayed (stack-like) on the map.
    """

    initial_center: MapLatitudeLongitude = field(
        default_factory=lambda: MapLatitudeLongitude(latitude=50.5, longitude=30.51)
    )
    """
    The initial center of the map.
    """

    initial_rotation: ft.Number = 0.0
    """
    The rotation (in degrees) when the map is first loaded.
    """

    initial_zoom: ft.Number = 13.0
    """
    The zoom when the map is first loaded.
    If initial_camera_fit is defined this has no effect.
    """

    interaction_configuration: InteractionConfiguration = field(
        default_factory=lambda: InteractionConfiguration()
    )
    """
    The interaction configuration.
    """

    bgcolor: ft.ColorValue = ft.Colors.GREY_300
    """
    The background color of this control.
    """

    keep_alive: bool = False
    """
    Whether to enable the built in keep-alive functionality.

    If the map is within a complex layout, such as a [`ListView`][flet.ListView],
    the map will reset to it's inital position after it appears back into view.
    To ensure this doesn't happen, enable this flag to prevent it from rebuilding.
    """

    max_zoom: Optional[ft.Number] = None
    """
    The maximum (highest) zoom level of every layer.
    Each layer can specify additional zoom level restrictions.
    """

    min_zoom: Optional[ft.Number] = None
    """
    The minimum (smallest) zoom level of every layer.
    Each layer can specify additional zoom level restrictions.
    """

    animation_curve: ft.AnimationCurve = ft.AnimationCurve.FAST_OUT_SLOWIN
    """
    The default animation curve to be used for map-animations
    when calling instance methods like [`zoom_in()`][(c).zoom_in],
    [`rotate_from()`][(c).rotate_from],
    [`move_to()`][(c).move_to] etc.
    """

    animation_duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration(milliseconds=500)
    )
    """
    The default animation duration to be used for map-animations
    when calling instance methods like [`zoom_in()`][(c).zoom_in],
    [`rotate_from()`][(c).rotate_from],
    [`move_to()`][(c).move_to] etc.
    """

    initial_camera_fit: Optional[CameraFit] = None
    """
    Defines the visible bounds when the map is first loaded.
    Takes precedence over [`initial_center`][(c).]/[`initial_zoom`][(c).].
    """

    on_init: Optional[ft.ControlEventHandler["Map"]] = None
    """
    Fires when the map is initialized.
    """

    on_tap: Optional[ft.EventHandler[MapTapEvent]] = None
    """
    Fires when a tap event occurs.
    """

    on_hover: Optional[ft.EventHandler[MapHoverEvent]] = None
    """
    Fires when a hover event occurs.
    """

    on_secondary_tap: Optional[ft.EventHandler[MapTapEvent]] = None
    """
    Fires when a secondary tap event occurs.
    """

    on_long_press: Optional[ft.EventHandler[MapTapEvent]] = None
    """
    Fires when a long press event occurs.
    """

    on_event: Optional[ft.EventHandler[MapEvent]] = None
    """
    Fires when any map events occurs.
    """

    on_position_change: Optional[ft.EventHandler[MapPositionChangeEvent]] = None
    """
    Fires when the map position changes.
    """

    on_pointer_down: Optional[ft.EventHandler[MapPointerEvent]] = None
    """
    Fires when a pointer down event occurs.
    """

    on_pointer_cancel: Optional[ft.EventHandler[MapPointerEvent]] = None
    """
    Fires when a pointer cancel event occurs.
    """

    on_pointer_up: Optional[ft.EventHandler[MapPointerEvent]] = None
    """
    Fires when a pointer up event occurs.
    """

    async def rotate_from(
        self,
        degree: ft.Number,
        animation_curve: Optional[ft.AnimationCurve] = None,
        animation_duration: Optional[ft.DurationValue] = None,
        cancel_ongoing_animations: bool = False,
    ) -> None:
        """
        Applies a rotation of `degree` to the current rotation.

        Args:
            degree: The number of degrees to increment to the current rotation.
            animation_curve: The curve of the animation. If None (the default),
                [`Map.animation_curve`][(p).] will be used.
            animation_duration: The duration of the animation.
                If None (the default), [`Map.animation_duration`][(p).] will be used.
            cancel_ongoing_animations: Whether to cancel/stop all
                ongoing map-animations before starting this new one.
        """
        await self._invoke_method(
            method_name="rotate_from",
            arguments={
                "degree": degree,
                "curve": animation_curve or self.animation_curve,
                "duration": animation_duration or self.animation_duration,
                "cancel_ongoing_animations": cancel_ongoing_animations,
            },
        )

    async def reset_rotation(
        self,
        animation_curve: Optional[ft.AnimationCurve] = None,
        animation_duration: Optional[ft.DurationValue] = None,
        cancel_ongoing_animations: bool = False,
    ) -> None:
        """
        Resets the map's rotation to 0 degrees.

        Args:
            animation_curve: The curve of the animation. If None (the default),
                [`Map.animation_curve`][(p).] will be used.
            animation_duration: The duration of the animation.
                If None (the default), [`Map.animation_duration`][(p).] will be used.
            cancel_ongoing_animations: Whether to cancel/stop all
                ongoing map-animations before starting this new one.
        """
        await self._invoke_method(
            method_name="reset_rotation",
            arguments={
                "curve": animation_curve or self.animation_curve,
                "duration": animation_duration or self.animation_duration,
                "cancel_ongoing_animations": cancel_ongoing_animations,
            },
        )

    async def zoom_in(
        self,
        animation_curve: Optional[ft.AnimationCurve] = None,
        animation_duration: Optional[ft.DurationValue] = None,
        cancel_ongoing_animations: bool = False,
    ) -> None:
        """
        Zooms in by one zoom-level from the current one.

        Args:
            animation_curve: The curve of the animation. If None (the default),
                [`Map.animation_curve`][(p).] will be used.
            animation_duration: The duration of the animation.
                If None (the default), [`Map.animation_duration`][(p).] will be used.
            cancel_ongoing_animations: Whether to cancel/stop all
                ongoing map-animations before starting this new one.
        """
        await self._invoke_method(
            method_name="zoom_in",
            arguments={
                "curve": animation_curve or self.animation_curve,
                "duration": animation_duration or self.animation_duration,
                "cancel_ongoing_animations": cancel_ongoing_animations,
            },
        )

    async def zoom_out(
        self,
        animation_curve: Optional[ft.AnimationCurve] = None,
        animation_duration: Optional[ft.DurationValue] = None,
        cancel_ongoing_animations: bool = False,
    ) -> None:
        """
        Zooms out by one zoom-level from the current one.

        Args:
            animation_curve: The curve of the animation. If `None` (the default),
                [`Map.animation_curve`][(p).] will be used.
            animation_duration: The duration of the animation.
                If None (the default), [`Map.animation_duration`][(p).] will be used.
            cancel_ongoing_animations: Whether to cancel/stop all
                ongoing map-animations before starting this new one.
        """
        await self._invoke_method(
            method_name="zoom_out",
            arguments={
                "curve": animation_curve or self.animation_curve,
                "duration": animation_duration or self.animation_duration,
                "cancel_ongoing_animations": cancel_ongoing_animations,
            },
        )

    async def zoom_to(
        self,
        zoom: ft.Number,
        animation_curve: Optional[ft.AnimationCurve] = None,
        animation_duration: Optional[ft.DurationValue] = None,
        cancel_ongoing_animations: bool = False,
    ) -> None:
        """
        Zoom the map to a specific zoom level.

        Args:
            zoom: The zoom level to zoom to.
            animation_curve: The curve of the animation. If `None` (the default),
                [`Map.animation_curve`][(p).] will be used.
            animation_duration: The duration of the animation.
                If None (the default), [`Map.animation_duration`][(p).] will be used.
            cancel_ongoing_animations: Whether to cancel/stop all
                ongoing map-animations before starting this new one.
        """
        await self._invoke_method(
            method_name="zoom_to",
            arguments={
                "zoom": zoom,
                "curve": animation_curve or self.animation_curve,
                "duration": animation_duration or self.animation_duration,
                "cancel_ongoing_animations": cancel_ongoing_animations,
            },
        )

    async def move_to(
        self,
        destination: Optional[MapLatitudeLongitude] = None,
        zoom: Optional[ft.Number] = None,
        rotation: Optional[ft.Number] = None,
        animation_curve: Optional[ft.AnimationCurve] = None,
        animation_duration: Optional[ft.DurationValue] = None,
        offset: ft.OffsetValue = (0, 0),
        cancel_ongoing_animations: bool = False,
    ) -> None:
        """
        Moves to a specific location.

        Args:
            destination: The destination point to move to.
            zoom: The zoom level to be applied. If provided,
                must be greater than or equal to `0.0`.
            rotation: Rotation (in degrees) to be applied.
            offset: The offset to be used. Only works when `rotation` is `None`.
            animation_curve: The curve of the animation. If None (the default),
                [`Map.animation_curve`][(p).] will be used.
            animation_duration: The duration of the animation.
                If None (the default), [`Map.animation_duration`][(p).] will be used.
            cancel_ongoing_animations: Whether to cancel/stop all
                ongoing map-animations before starting this new one.

        Raises:
            ValueError: If `zoom` is not `None` and is negative.
        """
        if zoom is not None and zoom < 0:
            raise ValueError(f"zoom must be greater than or equal to zero, got {zoom}")
        await self._invoke_method(
            method_name="move_to",
            arguments={
                "destination": destination,
                "zoom": zoom,
                "offset": offset,
                "rotation": rotation,
                "curve": animation_curve or self.animation_curve,
                "duration": animation_duration or self.animation_duration,
                "cancel_ongoing_animations": cancel_ongoing_animations,
            },
        )

    async def center_on(
        self,
        point: MapLatitudeLongitude,
        zoom: Optional[ft.Number],
        animation_curve: Optional[ft.AnimationCurve] = None,
        animation_duration: Optional[ft.DurationValue] = None,
        cancel_ongoing_animations: bool = False,
    ) -> None:
        """
        Centers the map on the given point.

        Args:
            point: The point on which to center the map.
            zoom: The zoom level to be applied.
            animation_curve: The curve of the animation. If `None` (the default),
                [`Map.animation_curve`][(p).] will be used.
            animation_duration: The duration of the animation.
                If None (the default), [`Map.animation_duration`][(p).] will be used.
            cancel_ongoing_animations: Whether to cancel/stop all
                ongoing map-animations before starting this new one.
        """
        await self._invoke_method(
            method_name="center_on",
            arguments={
                "point": point,
                "zoom": zoom,
                "curve": animation_curve or self.animation_curve,
                "duration": animation_duration or self.animation_duration,
                "cancel_ongoing_animations": cancel_ongoing_animations,
            },
        )
