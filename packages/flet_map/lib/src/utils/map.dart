import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

LatLng? parseLatLng(Control control, String propName, [LatLng? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return latLngFromJson(j1, defValue);
}

LatLng? latLngFromJson(Map<String, dynamic>? j, [LatLng? defValue]) {
  if (j == null) {
    return defValue;
  }
  return LatLng(
      parseDouble(j['latitude'], 0)!, parseDouble(j['longitude'], 0)!);
}

LatLngBounds? parseLatLngBounds(Control control, String propName,
    [LatLngBounds? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return latLngBoundsFromJson(j1, defValue);
}

LatLngBounds? latLngBoundsFromJson(Map<String, dynamic>? j,
    [LatLngBounds? defValue]) {
  if (j == null ||
      j['corner_1'] == null ||
      j['corner_2'] == null ||
      latLngFromJson(j['corner_1']) == null ||
      latLngFromJson(j['corner_2']) == null) {
    return defValue;
  }
  return LatLngBounds(
      latLngFromJson(j['corner_1'])!, latLngFromJson(j['corner_2'])!);
}

PatternFit? parsePatternFit(String? value,
    [PatternFit? defValue = PatternFit.none]) {
  if (value == null) {
    return defValue;
  }
  return PatternFit.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

StrokePattern? parseStrokePattern(Control control, String propName,
    [StrokePattern? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return strokePatternFromJson(j1, defValue);
}

StrokePattern? strokePatternFromJson(Map<String, dynamic>? j,
    [StrokePattern? defValue]) {
  if (j == null) {
    return defValue;
  }
  if (j['type'] == 'dotted') {
    return StrokePattern.dotted(
      spacingFactor: parseDouble(j['spacing_factor'], 1)!,
      patternFit: parsePatternFit(j['pattern_fit'], PatternFit.none)!,
    );
  } else if (j['type'] == 'solid') {
    return const StrokePattern.solid();
  } else if (j['type'] == 'dash') {
    var segments = j['segments'];
    return StrokePattern.dashed(
      patternFit: parsePatternFit(j['pattern_fit'], PatternFit.none)!,
      segments: segments != null
          ? (jsonDecode(segments) as List)
              .map((e) => parseDouble(e))
              .whereNotNull()
              .toList()
          : [],
    );
  }
  return defValue;
}

InteractionOptions? parseInteractionOptions(Control control, String propName,
    [InteractionOptions? defValue]) {
  var v = control.attrString(propName);
  if (v == null) {
    return defValue;
  }
  final j1 = json.decode(v);
  return interactionOptionsFromJSON(j1, defValue);
}

InteractionOptions? interactionOptionsFromJSON(dynamic j,
    [InteractionOptions? defValue]) {
  if (j == null) {
    return defValue;
  }
  return InteractionOptions(
      enableMultiFingerGestureRace:
          parseBool(j["enable_multi_finger_gesture_race"], false)!,
      pinchMoveThreshold: parseDouble(j["pinch_move_threshold"], 40.0)!,
      scrollWheelVelocity: parseDouble(j["scroll_wheel_velocity"], 0.005)!,
      pinchZoomThreshold: parseDouble(j["pinch_zoom_threshold"], 0.5)!,
      rotationThreshold: parseDouble(j["rotation_threshold"], 20.0)!,
      flags: parseInt(j["flags"], InteractiveFlag.all)!,
      rotationWinGestures:
          parseInt(j["rotation_win_gestures"], MultiFingerGesture.rotate)!,
      pinchMoveWinGestures: parseInt(j["pinch_move_win_gestures"],
          MultiFingerGesture.pinchZoom | MultiFingerGesture.pinchMove)!,
      pinchZoomWinGestures: parseInt(j["pinch_zoom_win_gestures"],
          MultiFingerGesture.pinchZoom | MultiFingerGesture.pinchMove)!);
}

EvictErrorTileStrategy? parseEvictErrorTileStrategy(String? strategy,
    [EvictErrorTileStrategy? defValue]) {
  if (strategy == null) {
    return defValue;
  }
  return EvictErrorTileStrategy.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == strategy.toLowerCase()) ??
      defValue;
}

MapOptions? parseConfiguration(Control control, String propName,
    FletControlBackend backend, ThemeData? theme,
    [MapOptions? defValue]) {
  var v = control.attrString(propName);
  if (v == null) {
    return defValue;
  }
  final j1 = json.decode(v);
  return configurationFromJSON(j1, control, backend, theme, defValue);
}

MapOptions? configurationFromJSON(
    dynamic j, Control control, FletControlBackend backend, ThemeData? theme,
    [MapOptions? defValue]) {
  if (j == null) {
    return defValue;
  }
  void triggerEvent(String name, dynamic eventData) {
    var d = "";
    if (eventData is String) {
      d = eventData;
    } else if (eventData is Map) {
      d = json.encode(eventData);
    }

    backend.triggerControlEvent(control.id, name, d);
  }

  return MapOptions(
    initialCenter:
        latLngFromJson(j["initial_center"], const LatLng(50.5, 30.51))!,
    interactionOptions: interactionOptionsFromJSON(
        j["interaction_configuration"], const InteractionOptions())!,
    backgroundColor: parseColor(theme, j['bgcolor'], const Color(0x00000000))!,
    initialRotation: parseDouble(j['initial_rotation'], 0.0)!,
    initialZoom: parseDouble(j['initial_zoom'], 13.0)!,
    keepAlive: parseBool(j['keep_alive'], false)!,
    maxZoom: parseDouble(j['max_zoom']),
    minZoom: parseDouble(j['min_zoom']),
    onPointerHover: control.attrBool("onHover", false)!
        ? (PointerHoverEvent e, LatLng latlng) {
            triggerEvent("hover", {
              "lat": latlng.latitude,
              "long": latlng.longitude,
              "gx": e.position.dx,
              "gy": e.position.dy,
              "lx": e.localPosition.dx,
              "ly": e.localPosition.dy,
              "kind": e.kind.name,
            });
          }
        : null,
    onTap: control.attrBool("onTap", false)!
        ? (TapPosition pos, LatLng latlng) {
            triggerEvent("tap", {
              "lat": latlng.latitude,
              "long": latlng.longitude,
              "gx": pos.global.dx,
              "gy": pos.global.dy,
              "lx": pos.relative?.dx,
              "ly": pos.relative?.dy,
            });
          }
        : null,
    onLongPress: control.attrBool("onLongPress", false)!
        ? (TapPosition pos, LatLng latlng) {
            triggerEvent("long_press", {
              "lat": latlng.latitude,
              "long": latlng.longitude,
              "gx": pos.global.dx,
              "gy": pos.global.dy,
              "lx": pos.relative?.dx,
              "ly": pos.relative?.dy,
            });
          }
        : null,
    onPositionChanged: control.attrBool("onPositionChange", false)!
        ? (MapCamera camera, bool hasGesture) {
            triggerEvent("position_change", {
              "lat": camera.center.latitude,
              "long": camera.center.longitude,
              "min_zoom": camera.minZoom,
              "max_zoom": camera.maxZoom,
              "rot": camera.rotation,
            });
          }
        : null,
    onPointerDown: control.attrBool("onPointerDown", false)!
        ? (PointerDownEvent e, LatLng latlng) {
            triggerEvent("pointer_down", {
              "lat": latlng.latitude,
              "long": latlng.longitude,
              "gx": e.position.dx,
              "gy": e.position.dy,
              "kind": e.kind.name,
            });
          }
        : null,
    onPointerCancel: control.attrBool("onPointerCancel", false)!
        ? (PointerCancelEvent e, LatLng latlng) {
            triggerEvent("pointer_cancel", {
              "lat": latlng.latitude,
              "long": latlng.longitude,
              "gx": e.position.dx,
              "gy": e.position.dy,
              "kind": e.kind.name,
            });
          }
        : null,
    onPointerUp: control.attrBool("onPointerUp", false)!
        ? (PointerUpEvent e, LatLng latlng) {
            triggerEvent("pointer_up", {
              "lat": latlng.latitude,
              "long": latlng.longitude,
              "gx": e.position.dx,
              "gy": e.position.dy,
              "kind": e.kind.name,
            });
          }
        : null,
    onSecondaryTap: control.attrBool("onSecondaryTap", false)!
        ? (TapPosition pos, LatLng latlng) {
            triggerEvent("secondary_tap", {
              "lat": latlng.latitude,
              "long": latlng.longitude,
              "gx": pos.global.dx,
              "gy": pos.global.dy,
              "lx": pos.relative?.dx,
              "ly": pos.relative?.dy,
            });
          }
        : null,
    onMapEvent: control.attrBool("onEvent", false)!
        ? (MapEvent e) {
            triggerEvent("event", {
              "src": e.source.name,
              "c_lat": e.camera.center.latitude,
              "c_long": e.camera.center.longitude,
              "zoom": e.camera.zoom,
              "min_zoom": e.camera.minZoom,
              "max_zoom": e.camera.maxZoom,
              "rot": e.camera.rotation,
            });
          }
        : null,
    onMapReady: control.attrBool("onInit", false)!
        ? () {
            debugPrint("Map ${control.id} init");
            backend.triggerControlEvent(control.id, "init");
          }
        : null,
  );
}
