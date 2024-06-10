import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
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

BorderRadius borderRadiusFromJSON(dynamic json) {
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

Border borderFromJSON(ThemeData? theme, Map<String, dynamic> json,
    [Color? defaultSideColor]) {
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
          style: BorderStyle.solid)
      : null;
}

OutlinedBorder? outlinedBorderFromJSON(Map<String, dynamic> json) {
  String type = json["type"];
  if (type == "roundedRectangle") {
    return RoundedRectangleBorder(
        borderRadius: json["radius"] != null
            ? borderRadiusFromJSON(json["radius"])
            : BorderRadius.zero);
  } else if (type == "stadium") {
    return const StadiumBorder();
  } else if (type == "circle") {
    return const CircleBorder();
  } else if (type == "beveledRectangle") {
    return BeveledRectangleBorder(
        borderRadius: json["radius"] != null
            ? borderRadiusFromJSON(json["radius"])
            : BorderRadius.zero);
  } else if (type == "continuousRectangle") {
    return ContinuousRectangleBorder(
        borderRadius: json["radius"] != null
            ? borderRadiusFromJSON(json["radius"])
            : BorderRadius.zero);
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
    j = {"": j};
  }

  return WidgetStateBorderSideFromJSON(
      j, (jv) => borderSideFromJSON(theme, jv, null), BorderSide.none);
}

class WidgetStateBorderSideFromJSON extends WidgetStateBorderSide {
  late final Map<String, BorderSide?> _states;
  late final BorderSide _defaultValue;

  WidgetStateBorderSideFromJSON(
      Map<String, dynamic>? jsonDictValue,
      BorderSide? Function(dynamic) converterFromJson,
      BorderSide defaultValue) {
    _defaultValue = defaultValue;
    _states = {};
    if (jsonDictValue != null) {
      jsonDictValue.forEach((stateStr, jv) {
        stateStr.split(",").map((s) => s.trim().toLowerCase()).forEach((state) {
          _states[state] = converterFromJson(jv);
        });
      });
    }
  }

  @override
  BorderSide? resolve(Set<WidgetState> states) {
    // find specific state
    for (var state in states) {
      if (_states.containsKey(state.name)) {
        return _states[state.name];
      }
    }

    // catch-all value
    if (_states.containsKey("")) {
      return _states[""];
    }

    return _defaultValue;
  }
}
