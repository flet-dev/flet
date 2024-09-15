import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
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
