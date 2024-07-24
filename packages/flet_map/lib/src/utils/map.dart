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
  return latLngFromJson(j1);
}

LatLng latLngFromJson(Map<String, dynamic> json) {
  return LatLng(
      parseDouble(json['latitude'], 0)!, parseDouble(json['longitude'], 0)!);
}

LatLngBounds? parseLatLngBounds(Control control, String propName,
    [LatLngBounds? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return latLngBoundsFromJson(j1);
}

LatLngBounds? latLngBoundsFromJson(Map<String, dynamic> json) {
  if (json['corner_1'] == null || json['corner_2'] == null) {
    return null;
  }
  return LatLngBounds(
      latLngFromJson(json['corner_1']), latLngFromJson(json['corner_2']));
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
  return strokePatternFromJson(j1);
}

StrokePattern? strokePatternFromJson(Map<String, dynamic> json) {
  if (json['type'] == 'dotted') {
    return StrokePattern.dotted(
      spacingFactor: parseDouble(json['spacing_factor'], 1)!,
      patternFit: parsePatternFit(json['pattern_fit'], PatternFit.none)!,
    );
  } else if (json['type'] == 'solid') {
    return const StrokePattern.solid();
  } else if (json['type'] == 'dash') {
    var segments = json['segments'];
    return StrokePattern.dashed(
      patternFit: parsePatternFit(json['pattern_fit'], PatternFit.none)!,
      segments: segments != null
          ? (jsonDecode(segments) as List)
              .map((e) => parseDouble(e))
              .whereNotNull()
              .toList()
          : [],
    );
  }
  return null;
}

InteractionOptions parseInteractionOptions(Control control, String propName,
    [InteractionOptions defValue = const InteractionOptions()]) {
  var v = control.attrString(propName);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return interactionOptionsFromJSON(j1);
}

InteractionOptions interactionOptionsFromJSON(dynamic json) {
  return InteractionOptions(
      enableMultiFingerGestureRace:
          parseBool(json["enable_multi_finger_gesture_race"], false)!,
      pinchMoveThreshold: parseDouble(json["pinch_move_threshold"], 40.0)!,
      scrollWheelVelocity: parseDouble(json["scroll_wheel_velocity"], 0.005)!,
      pinchZoomThreshold: parseDouble(json["pinch_zoom_threshold"], 0.5)!,
      rotationThreshold: parseDouble(json["rotation_threshold"], 20.0)!,
      flags: parseInt(json["flags"], InteractiveFlag.all)!,
      rotationWinGestures:
          parseInt(json["rotation_win_gestures"], MultiFingerGesture.rotate)!,
      pinchMoveWinGestures: parseInt(json["pinch_move_win_gestures"],
          MultiFingerGesture.pinchZoom | MultiFingerGesture.pinchMove)!,
      pinchZoomWinGestures: parseInt(json["pinch_zoom_win_gestures"],
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
