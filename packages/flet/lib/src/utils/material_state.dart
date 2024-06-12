import 'package:flutter/material.dart';

WidgetStateProperty<T?>? getWidgetStateProperty<T>(
    dynamic jsonDictValue, T Function(dynamic) converterFromJson,
    [T? defaultValue]) {
  if (jsonDictValue == null) {
    return null;
  }
  var j = jsonDictValue;
  if (j is! Map<String, dynamic>) {
    j = {"": j};
  }
  return WidgetStateFromJSON(j, converterFromJson, defaultValue);
}

class WidgetStateFromJSON<T> extends WidgetStateProperty<T?> {
  late final Map<String, T> _states;
  late final T? _defaultValue;

  WidgetStateFromJSON(Map<String, dynamic>? jsonDictValue,
      T Function(dynamic) converterFromJson, T? defaultValue) {
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
  T? resolve(Set<WidgetState> states) {
    //debugPrint("WidgetStateFromJSON states: $states, _states: $_states");
    // find specific state
    for (var state in states) {
      if (_states.containsKey(state.name)) {
        return _states[state.name]!;
      }
    }

    // catch-all value
    if (_states.containsKey("")) {
      return _states[""];
    }

    return _defaultValue;
  }
}
