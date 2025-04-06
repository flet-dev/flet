import 'dart:collection';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
import 'material_state.dart';
import 'numbers.dart';

BorderRadius? parseBorderRadius(Control control, String propName,
    [BorderRadius? defaultValue]) {
  var v = control.get(propName);
  if (v == null) {
    return defaultValue;
  }
  return borderRadiusFromJSON(v);
}

Radius? parseRadius(Control control, String propName, [Radius? defaultValue]) {
  var r = control.get<double>(propName);
  if (r == null) {
    return defaultValue;
  }

  return Radius.circular(r);
}

Border? parseBorder(ThemeData theme, Control control, String propName,
    [Color? defaultSideColor]) {
  var v = control.get(
    propName,
  );
  if (v == null) {
    return null;
  }
  return borderFromJSON(theme, v, defaultSideColor);
}

BorderSide? parseBorderSide(ThemeData theme, Control control, String propName,
    {Color? defaultSideColor}) {
  var v = control.get(propName);
  if (v == null) {
    return null;
  }
  return borderSideFromJSON(theme, v, defaultSideColor);
}

OutlinedBorder? parseOutlinedBorder(Control control, String propName) {
  var v = control.get(propName);
  if (v == null) {
    return null;
  }
  return outlinedBorderFromJSON(v);
}

BorderRadius? borderRadiusFromJSON(dynamic json, [BorderRadius? defaultValue]) {
  if (json == null) {
    return defaultValue;
  }
  if (json is int || json is double) {
    return BorderRadius.all(Radius.circular(parseDouble(json, 0)!));
  }
  return BorderRadius.only(
    topLeft: Radius.circular(parseDouble(json['top_left'], 0)!),
    topRight: Radius.circular(parseDouble(json['top_right'], 0)!),
    bottomLeft: Radius.circular(parseDouble(json['bottom_left'], 0)!),
    bottomRight: Radius.circular(parseDouble(json['bottom_right'], 0)!),
  );
}

Border? borderFromJSON(ThemeData? theme, Map<dynamic, dynamic>? json,
    [Color? defaultSideColor, Border? defaultBorder]) {
  if (json == null) {
    return defaultBorder;
  }
  return Border(
      top: borderSideFromJSON(theme, json['top'], defaultSideColor) ??
          BorderSide.none,
      right: borderSideFromJSON(theme, json['right'], defaultSideColor) ??
          BorderSide.none,
      bottom: borderSideFromJSON(theme, json['bottom'], defaultSideColor) ??
          BorderSide.none,
      left: borderSideFromJSON(theme, json['left'], defaultSideColor) ??
          BorderSide.none);
}

BorderSide? borderSideFromJSON(ThemeData? theme, dynamic json,
    [Color? defaultSideColor]) {
  return json != null
      ? BorderSide(
          color: parseColor(
              theme, json['color'], defaultSideColor ?? Colors.black)!,
          width: parseDouble(json['width'], 1)!,
          strokeAlign:
              parseDouble(json['stroke_align'], BorderSide.strokeAlignInside)!,
          style: BorderStyle.solid)
      : null;
}

OutlinedBorder? outlinedBorderFromJSON(Map<dynamic, dynamic>? json) {
  if (json == null) {
    return null;
  }

  String type = json["type"];
  if (type == "roundedRectangle") {
    return RoundedRectangleBorder(
        borderRadius: borderRadiusFromJSON(json["radius"], BorderRadius.zero)!);
  } else if (type == "stadium") {
    return const StadiumBorder();
  } else if (type == "circle") {
    return const CircleBorder();
  } else if (type == "beveledRectangle") {
    return BeveledRectangleBorder(
        borderRadius: borderRadiusFromJSON(json["radius"], BorderRadius.zero)!);
  } else if (type == "continuousRectangle") {
    return ContinuousRectangleBorder(
        borderRadius: borderRadiusFromJSON(json["radius"], BorderRadius.zero)!);
  }
  return null;
}

WidgetStateBorderSide? parseWidgetStateBorderSide(
    ThemeData theme, Control control, String propName) {
  var v = control.get(propName);
  if (v == null) {
    return null;
  }
  if (v is Map<String, dynamic> &&
      (v.containsKey("width") || v.containsKey("color"))) {
    v = {"default": v};
  }

  return WidgetStateBorderSideFromJSON(
      v, (jv) => borderSideFromJSON(theme, jv), BorderSide.none);
}

class WidgetStateBorderSideFromJSON extends WidgetStateBorderSide {
  late final Map<String, BorderSide?> _states;
  late final BorderSide _defaultValue;

  WidgetStateBorderSideFromJSON(
      Map<String, dynamic>? jsonDictValue,
      BorderSide? Function(dynamic) converterFromJson,
      BorderSide defaultValue) {
    _defaultValue = defaultValue;

    // preserve user-defined order
    _states = LinkedHashMap<String, BorderSide?>.from(
      jsonDictValue?.map((k, v) {
            var key = k.trim().toLowerCase();
            // "" is deprecated and renamed to "default"
            if (key == "") key = "default";
            return MapEntry(key, converterFromJson(v));
          }) ??
          {},
    );
  }

  @override
  BorderSide? resolve(Set<WidgetState> states) {
    // Resolve using user-defined order in _states
    for (var stateName in _states.keys) {
      if (stateName == "default") continue; // Skip "default"; handled last
      if (states.any((state) => state.name == stateName)) {
        return _states[stateName];
      }
    }

    // Default state
    return _states["default"] ?? _defaultValue;
  }
}

WidgetStateProperty<OutlinedBorder?>? parseWidgetStateOutlinedBorder(
    Control control, String propName) {
  var v = control.get<String>(propName, null);
  if (v == null) {
    return null;
  }

  return getWidgetStateProperty<OutlinedBorder?>(
      v, (jv) => outlinedBorderFromJSON(jv), null);
}
