import 'dart:convert';

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
      foregroundColor: MaterialStateFromJSON<Color?>(
          json["color"],
          (jv) => HexColor.fromString(theme, jv as String),
          theme.colorScheme.primary),
      backgroundColor: MaterialStateFromJSON<Color?>(
          json["bgcolor"],
          (jv) => HexColor.fromString(theme, jv as String),
          theme.colorScheme.surface));
}

class MaterialStateFromJSON<T> extends MaterialStateProperty<T> {
  late final Map<String, T> _states;
  late final T _defaultValue;
  MaterialStateFromJSON(Map<String, dynamic> jsonValue,
      T Function(dynamic) converterFromJson, T defaultValue) {
    _defaultValue = defaultValue;
    _states = {};
    jsonValue.forEach((stateStr, jv) {
      stateStr.split(",").map((s) => s.trim().toLowerCase()).forEach((state) {
        _states[state] = converterFromJson(jv);
      });
    });
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
