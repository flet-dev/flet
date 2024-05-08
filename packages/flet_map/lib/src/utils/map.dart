import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

MapOptions parseMapOptions(
    Control control, String propName, BuildContext context) {
  var v = control.attrString(propName);
  if (v == null) {
    return const MapOptions();
  }
  ThemeData theme = Theme.of(context);

  final j1 = json.decode(v);
  return mapOptionsFromJSON(j1, theme);
}

MapOptions mapOptionsFromJSON(dynamic json, ThemeData theme) {
  return MapOptions(
    applyPointerTranslucencyToLayers:
        parseBool(json["apply_pointer_translucency_to_layers"], true),
    backgroundColor:
        parseColorFromJson(theme, json["bgcolor"]) ?? const Color(0xFFE0E0E0),
    initialCenter: json["initial_center"] != null
        ? LatLng(parseDouble(json["initial_center"][0], 50.5),
            parseDouble(json["initial_center"][1], 30.51))
        : const LatLng(50.5, 30.51),
    initialRotation: parseDouble(json["initial_rotation"], 0.0),
    initialZoom: parseDouble(json["initial_zoom"], 13.0),
    keepAlive: parseBool(json["keep_alive"], false),
    maxZoom: json["max_zoom"] != null ? parseDouble(json["max_zoom"]) : null,
    minZoom: json["min_zoom"] != null ? parseDouble(json["min_zoom"]) : null,
    // interactionOptions: ,
    // cameraConstraint: ,
    // crs: ,
    // initialCameraFit: ,
  );
}

LatLng? parseLatLng(Control control, String propName, [LatLng? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return latLngFromJson(j1);
}

LatLng latLngFromJson(Map<String, dynamic> json) {
  return LatLng(parseDouble(json['latitude']), parseDouble(json['longitude']));
}

InteractionOptions? parseInteractionOptions(Control control, String propName) {
  var v = control.attrString(propName);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return interactionOptionsFromJSON(j1);
}

InteractionOptions interactionOptionsFromJSON(dynamic json) {
  return InteractionOptions(
      enableMultiFingerGestureRace:
          parseBool(json["enable_multi_finger_gesture_race"], false),
      enableScrollWheel: parseBool(json["enable_scroll_wheel"], false),
      pinchMoveThreshold: parseDouble(json["pinch_move_threshold"], 40.0),
      scrollWheelVelocity: parseDouble(json["scroll_wheel_velocity"], 0.005),
      pinchZoomThreshold: parseDouble(json["pinch_zoom_threshold"], 0.5),
      rotationThreshold: parseDouble(json["rotation_threshold"], 20.0)
      // flags: json["flags"] ? parseInt(json["flags"]) : InteractiveFlag.all,
      // rotationWinGestures: ,
      // pinchMoveWinGestures: ,
      // pinchZoomWinGestures: ,
      );
}
