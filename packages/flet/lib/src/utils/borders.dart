import 'dart:collection';
import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
import 'material_state.dart';
import 'numbers.dart';

BorderRadius? parseBorderRadius(Control control, String propName,
    [BorderRadius? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return borderRadiusFromJSON(j1);
}

Radius? parseRadius(Control control, String propName, [Radius? defaultValue]) {
  var r = control.attrDouble(propName, null);
  if (r == null) {
    return defaultValue;
  }

  return Radius.circular(r);
}

Border? parseBorder(ThemeData theme, Control control, String propName,
    [Color? defaultSideColor]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return borderFromJSON(theme, j1, defaultSideColor);
}

BorderSide? parseBorderSide(ThemeData theme, Control control, String propName,
    {Color? defaultSideColor}) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return borderSideFromJSON(theme, j1, defaultSideColor);
}

OutlinedBorder? parseOutlinedBorder(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return outlinedBorderFromJSON(j1);
}

BorderRadius? borderRadiusFromJSON(dynamic json, [BorderRadius? defaultValue]) {
  if (json == null) {
    return defaultValue;
  }
  if (json is int || json is double) {
    return BorderRadius.all(Radius.circular(parseDouble(json, 0)!));
  }
  return BorderRadius.only(
    topLeft: Radius.circular(parseDouble(json['tl'], 0)!),
    topRight: Radius.circular(parseDouble(json['tr'], 0)!),
    bottomLeft: Radius.circular(parseDouble(json['bl'], 0)!),
    bottomRight: Radius.circular(parseDouble(json['br'], 0)!),
  );
}

Border? borderFromJSON(ThemeData? theme, Map<String, dynamic>? json,
    [Color? defaultSideColor, Border? defaultBorder]) {
  if (json == null) {
    return defaultBorder;
  }
  return Border(
      top: borderSideFromJSON(theme, json['t'], defaultSideColor) ??
          BorderSide.none,
      right: borderSideFromJSON(theme, json['r'], defaultSideColor) ??
          BorderSide.none,
      bottom: borderSideFromJSON(theme, json['b'], defaultSideColor) ??
          BorderSide.none,
      left: borderSideFromJSON(theme, json['l'], defaultSideColor) ??
          BorderSide.none);
}

BorderSide? borderSideFromJSON(ThemeData? theme, dynamic json,
    [Color? defaultSideColor]) {
  return json != null
      ? BorderSide(
          color:
              parseColor(theme, json['c'], defaultSideColor ?? Colors.black)!,
          width: parseDouble(json['w'], 1)!,
          strokeAlign: parseDouble(json['sa'], BorderSide.strokeAlignInside)!,
          style: BorderStyle.solid)
      : null;
}

OutlinedBorder? outlinedBorderFromJSON(Map<String, dynamic>? json) {
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
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  var j = json.decode(v);
  if (j is Map<String, dynamic> && (j.containsKey("w") || j.containsKey("c"))) {
    j = {"default": j};
  }

  return WidgetStateBorderSideFromJSON(
      j, (jv) => borderSideFromJSON(theme, jv), BorderSide.none);
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
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  return getWidgetStateProperty<OutlinedBorder?>(
      jsonDecode(v), (jv) => outlinedBorderFromJSON(jv), null);
}
