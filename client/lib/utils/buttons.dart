import 'dart:convert';

import 'package:flet_view/utils/borders.dart';
import 'package:flet_view/utils/edge_insets.dart';
import 'package:flet_view/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';

ButtonStyle? parseButtonStyle(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return buttonStyleFromJSON(theme, j1);
}

ButtonStyle? buttonStyleFromJSON(ThemeData theme, Map<String, dynamic> json) {
  return ButtonStyle(
      foregroundColor: getMaterialStateProperty(
          json["color"],
          (jv) => HexColor.fromString(theme, jv as String),
          theme.colorScheme.primary),
      backgroundColor: getMaterialStateProperty(
          json["bgcolor"],
          (jv) => HexColor.fromString(theme, jv as String),
          theme.colorScheme.surface),
      overlayColor: getMaterialStateProperty(
          json["overlay_color"],
          (jv) => HexColor.fromString(theme, jv as String),
          theme.colorScheme.primary.withOpacity(0.08)),
      shadowColor: getMaterialStateProperty(
          json["shadow_color"],
          (jv) => HexColor.fromString(theme, jv as String),
          theme.colorScheme.shadow),
      surfaceTintColor: getMaterialStateProperty(
          json["surface_tint_color"],
          (jv) => HexColor.fromString(theme, jv as String),
          theme.colorScheme.surfaceTint),
      elevation: getMaterialStateProperty(
          json["elevation"], (jv) => parseDouble(jv), 1),
      animationDuration: json["animation_duration"] != null
          ? Duration(milliseconds: parseInt(json["animation_duration"][""]))
          : null,
      padding: getMaterialStateProperty(
          json["padding"],
          (jv) => edgeInsetsFromJson(jv),
          const EdgeInsets.symmetric(horizontal: 8)),
      side: getMaterialStateProperty(
          json["side"],
          (jv) => borderSideFromJSON(theme, jv, theme.colorScheme.outline),
          BorderSide.none),
      shape: getMaterialStateProperty(json["shape"],
          (jv) => outlinedBorderFromJSON(jv), const StadiumBorder()));
}

MaterialStateProperty<T>? getMaterialStateProperty<T>(
    Map<String, dynamic>? jsonDictValue,
    T Function(dynamic) converterFromJson,
    T defaultValue) {
  if (jsonDictValue == null) {
    return null;
  }
  return MaterialStateFromJSON(jsonDictValue, converterFromJson, defaultValue);
}

class MaterialStateFromJSON<T> extends MaterialStateProperty<T> {
  late final Map<String, T> _states;
  late final T _defaultValue;
  MaterialStateFromJSON(Map<String, dynamic>? jsonDictValue,
      T Function(dynamic) converterFromJson, T defaultValue) {
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
  T resolve(Set<MaterialState> states) {
    //debugPrint("MaterialStateFromJSON states: $states, _states: $_states");
    // find specific state
    for (var state in states) {
      if (_states.containsKey(state.name)) {
        return _states[state.name]!;
      }
    }

    // catch-all value
    if (_states.containsKey("")) {
      return _states[""]!;
    }

    return _defaultValue;
  }
}
