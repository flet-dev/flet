import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

LatLng? parseLatLng(dynamic value, [LatLng? defaultValue]) {
  if (value == null) return defaultValue;

  return LatLng(
      parseDouble(value['latitude'], 0)!, parseDouble(value['longitude'], 0)!);
}

LatLngBounds? parseLatLngBounds(dynamic value, [LatLngBounds? defaultValue]) {
  if (value == null ||
      value['corner_1'] == null ||
      value['corner_2'] == null ||
      parseLatLng(value['corner_1']) == null ||
      parseLatLng(value['corner_2']) == null) {
    return defaultValue;
  }
  return LatLngBounds(
      parseLatLng(value['corner_1'])!, parseLatLng(value['corner_2'])!);
}

PatternFit? parsePatternFit(String? value, [PatternFit? defaultValue]) {
  if (value == null) return defaultValue;
  return PatternFit.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

StrokePattern? parseStrokePattern(dynamic value,
    [StrokePattern? defaultValue]) {
  if (value == null) return defaultValue;
  final type = value['_type'];
  if (type == 'dotted') {
    return StrokePattern.dotted(
      spacingFactor: parseDouble(value['spacing_factor'], 1.5)!,
      patternFit: parsePatternFit(value['pattern_fit'], PatternFit.scaleUp)!,
    );
  } else if (type == 'solid') {
    return const StrokePattern.solid();
  } else if (type == 'dashed') {
    var segments = value['segments'] ?? [];
    return StrokePattern.dashed(
      patternFit: parsePatternFit(value['pattern_fit'], PatternFit.scaleUp)!,
      segments: segments.map((e) => parseDouble(e)).nonNulls.toList(),
    );
  }
  return defaultValue;
}

TileDisplay? parseTileDisplay(dynamic value, [TileDisplay? defaultValue]) {
  if (value == null) return defaultValue;
  final type = value['_type'];
  if (type == 'instantaneous') {
    return TileDisplay.instantaneous(
      opacity: parseDouble(value['opacity'], 1.0)!,
    );
  } else if (type == 'fadein') {
    return TileDisplay.fadeIn(
      startOpacity: parseDouble(value['start_opacity'], 1.0)!,
      reloadStartOpacity: parseDouble(value['reload_start_opacity'], 1.0)!,
      duration:
          parseDuration(value['duration'], const Duration(milliseconds: 100))!,
    );
  }
  return defaultValue;
}

InteractionOptions? parseInteractionOptions(dynamic value,
    [InteractionOptions? defaultValue]) {
  if (value == null) return defaultValue;
  return InteractionOptions(
    enableMultiFingerGestureRace:
        parseBool(value["enable_multi_finger_gesture_race"], false)!,
    pinchMoveThreshold: parseDouble(
      value["pinch_move_threshold"],
    )!,
    scrollWheelVelocity: parseDouble(value["scroll_wheel_velocity"], 0.005)!,
    pinchZoomThreshold: parseDouble(value["pinch_zoom_threshold"], 0.5)!,
    rotationThreshold: parseDouble(value["rotation_threshold"], 20.0)!,
    flags: parseInt(value["flags"], InteractiveFlag.all)!,
    rotationWinGestures:
        parseInt(value["rotation_win_gestures"], MultiFingerGesture.rotate)!,
    pinchMoveWinGestures: parseInt(value["pinch_move_win_gestures"],
        MultiFingerGesture.pinchZoom | MultiFingerGesture.pinchMove)!,
    pinchZoomWinGestures: parseInt(value["pinch_zoom_win_gestures"],
        MultiFingerGesture.pinchZoom | MultiFingerGesture.pinchMove)!,
    keyboardOptions: parseKeyboardOptions(
        value["keyboard_configuration"], const KeyboardOptions())!,
    cursorKeyboardRotationOptions: parseCursorKeyboardRotationOptions(
        value["cursor_keyboard_rotation_configuration"],
        const CursorKeyboardRotationOptions())!,
  );
}

CameraFit? parseCameraFit(dynamic value, [CameraFit? defaultValue]) {
  if (value == null) return defaultValue;

  final bounds = parseLatLngBounds(value["bounds"]);
  final coordinates = (value["coordinates"] as List?)
      ?.map((c) => parseLatLng(c))
      .nonNulls
      .toList();
  if (bounds == null && coordinates == null) return defaultValue;

  final forceIntegerZoomLevel =
      parseBool(value["force_integer_zoom_level"], false)!;
  final maxZoom = parseDouble(value["max_zoom"]);
  final minZoom = parseDouble(value["min_zoom"], 0)!;
  final padding = parsePadding(value["padding"], EdgeInsets.zero)!;
  if (bounds != null) {
    return CameraFit.insideBounds(
      bounds: bounds,
      forceIntegerZoomLevel: forceIntegerZoomLevel,
      maxZoom: maxZoom,
      minZoom: minZoom,
      padding: padding,
    );
  } else {
    return CameraFit.coordinates(
      coordinates: coordinates!,
      forceIntegerZoomLevel: forceIntegerZoomLevel,
      maxZoom: maxZoom,
      minZoom: minZoom,
      padding: padding,
    );
  }
}

KeyboardOptions? parseKeyboardOptions(dynamic value,
    [KeyboardOptions? defaultValue]) {
  if (value == null) return defaultValue;
  return KeyboardOptions(
      autofocus: parseBool(value["autofocus"], true)!,
      animationCurveDuration: parseDuration(value["animation_curve_duration"],
          const Duration(milliseconds: 450))!,
      animationCurveCurve:
          parseCurve(value["animation_curve_curve"], Curves.easeInOut)!,
      enableArrowKeysPanning:
          parseBool(value["enable_arrow_keys_panning"], true)!,
      enableQERotating: parseBool(value["enable_qe_rotating"], true)!,
      enableRFZooming: parseBool(value["enable_rf_zooming"], true)!,
      enableWASDPanning: parseBool(value["enable_wasd_panning"], true)!,
      leapMaxOfCurveComponent:
          parseDouble(value["leap_max_of_curve_component"], 0.6)!,
      // maxPanVelocity: ,
      maxRotateVelocity: parseDouble(value["max_rotate_velocity"], 3)!,
      maxZoomVelocity: parseDouble(value["max_zoom_velocity"], 0.03)!,
      panLeapVelocityMultiplier:
          parseDouble(value["pan_leap_velocity_multiplier"], 5)!,
      rotateLeapVelocityMultiplier:
          parseDouble(value["rotate_leap_velocity_multiplier"], 3)!,
      zoomLeapVelocityMultiplier:
          parseDouble(value["zoom_leap_velocity_multiplier"], 3)!,
      performLeapTriggerDuration:
          parseDuration(value["perform_leap_trigger_duration"]),
      animationCurveReverseDuration:
          parseDuration(value["animation_curve_reverse_duration"]));
}

CursorRotationBehaviour? parseCursorRotationBehaviour(String? value,
    [CursorRotationBehaviour? defValue]) {
  if (value == null) return defValue;
  return CursorRotationBehaviour.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

CursorKeyboardRotationOptions? parseCursorKeyboardRotationOptions(dynamic value,
    [CursorKeyboardRotationOptions? defaultValue]) {
  if (value == null) return defaultValue;
  return CursorKeyboardRotationOptions(
      setNorthOnClick: parseBool(value["set_north_on_click"], true)!,
      behaviour: parseCursorRotationBehaviour(
          value["behaviour"], CursorRotationBehaviour.offset)!,
      isKeyTrigger: (LogicalKeyboardKey key) {
        return (value["trigger_keys"] as List).contains(key);
      });
}

// Crs? parseCrs(dynamic value, [Crs? defaultValue]) {
//   if (value == null) return defaultValue;
//   return Crs();
// }

// MapCamera? parseMapCamera(dynamic value, [MapCamera? defaultValue]) {
//   if (value == null) return defaultValue;
//   return MapCamera(
//     crs: Crs(),
//     center: parseLatLng(value["center"])!,
//     zoom: parseDouble(value["zoom"], 0)!,
//     minZoom: parseDouble(value["min_zoom"], 0)!,
//     maxZoom: parseDouble(value["max_zoom"], 0)!,
//     rotation: parseDouble(value["rotation"], 0)!,
//     bounds: parseLatLngBounds(value["bounds"]),
//   );
// }

EvictErrorTileStrategy? parseEvictErrorTileStrategy(String? value,
    [EvictErrorTileStrategy? defaultValue]) {
  if (value == null) return defaultValue;
  return EvictErrorTileStrategy.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

extension TapPositionExtension on TapPosition {
  Map<String, dynamic> toMap() => {
        "gx": global.dx,
        "gy": global.dy,
        "lx": relative?.dx,
        "ly": relative?.dy,
      };
}

extension LatLngExtension on LatLng {
  Map<String, dynamic> toMap() => {
        "latitude": latitude,
        "longitude": longitude,
      };
}

extension LatLngBoundsExtension on LatLngBounds {
  // TODO
  // Map<String, dynamic> toMap() => {
  //
  //     };
}

extension MapCameraExtension on MapCamera {
  Map<String, dynamic> toMap() => {
        "center": center.toMap(),
        "zoom": zoom,
        "min_zoom": minZoom,
        "max_zoom": maxZoom,
        "rotation": rotation,
      };
}

extension MapEventExtension on MapEvent {
  Map<String, dynamic> toMap() => {
        "source": source.name,
        "camera": camera.toMap(),
      };
}

MapOptions? parseConfiguration(Control control, BuildContext context,
    [MapOptions? defaultValue]) {
  return MapOptions(
    initialCenter:
        parseLatLng(control.get("initial_center"), const LatLng(50.5, 30.51))!,
    interactionOptions: parseInteractionOptions(
        control.get("interaction_configuration"), const InteractionOptions())!,
    backgroundColor: control.getColor("bgcolor", context, Colors.grey[300])!,
    initialRotation: control.getDouble("initial_rotation", 0.0)!,
    initialZoom: control.getDouble("initial_zoom", 13.0)!,
    keepAlive: control.getBool("keep_alive", false)!,
    maxZoom: control.getDouble("max_zoom"),
    minZoom: control.getDouble("min_zoom"),
    initialCameraFit: parseCameraFit(control.get("initial_camera_fit")),
    onPointerHover: control.getBool("on_hover", false)!
        ? (PointerHoverEvent e, LatLng latlng) {
            control.triggerEvent("hover", {
              "coordinates": latlng.toMap(),
              ...e.toMap(),
            });
          }
        : null,
    onTap: control.getBool("on_tap", false)!
        ? (TapPosition pos, LatLng latlng) {
            control.triggerEvent("tap", {
              "coordinates": latlng.toMap(),
              ...pos.toMap(),
            });
          }
        : null,
    onLongPress: control.getBool("on_long_press", false)!
        ? (TapPosition pos, LatLng latlng) {
            control.triggerEvent("long_press", {
              "coordinates": latlng.toMap(),
              ...pos.toMap(),
            });
          }
        : null,
    onPositionChanged: control.getBool("on_position_change", false)!
        ? (MapCamera camera, bool hasGesture) {
            control.triggerEvent("position_change", {
              "coordinates": camera.center.toMap(),
              "has_gesture": hasGesture,
              "camera": camera.toMap()
            });
          }
        : null,
    onPointerDown: control.getBool("on_pointer_down", false)!
        ? (PointerDownEvent e, LatLng latlng) {
            control.triggerEvent("pointer_down", {
              "coordinates": latlng.toMap(),
              ...e.toMap(),
            });
          }
        : null,
    onPointerCancel: control.getBool("on_pointer_cancel", false)!
        ? (PointerCancelEvent e, LatLng latlng) {
            control.triggerEvent("pointer_cancel", {
              "coordinates": latlng.toMap(),
              ...e.toMap(),
            });
          }
        : null,
    onPointerUp: control.getBool("on_pointer_up", false)!
        ? (PointerUpEvent e, LatLng latlng) {
            control.triggerEvent(
                "pointer_up", {"coordinates": latlng.toMap(), ...e.toMap()});
          }
        : null,
    onSecondaryTap: control.getBool("on_secondary_tap", false)!
        ? (TapPosition pos, LatLng latlng) {
            control.triggerEvent("secondary_tap", {
              "coordinates": latlng.toMap(),
              ...pos.toMap(),
            });
          }
        : null,
    onMapEvent: control.getBool("on_event", false)!
        ? (MapEvent e) => control.triggerEvent("event", e.toMap())
        : null,
    onMapReady: control.getBool("on_init", false)!
        ? () => control.triggerEvent("init")
        : null,
  );
}
