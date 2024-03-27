import 'package:flutter/material.dart';

MaterialStateProperty<T?>? getMaterialStateProperty<T>(dynamic jsonDictValue, T Function(dynamic) converterFromJson,
    [T? defaultValue]) {
  if (jsonDictValue == null) {
    return null;
  }
  var j = jsonDictValue;
  if (j is! Map<String, dynamic>) {
    j = {"": j};
  }
  return MaterialStateFromJSON(j, converterFromJson, defaultValue);
}

class MaterialStateFromJSON<T> extends MaterialStateProperty<T?> {
  late final Map<String, T> _states;
  late final T? _defaultValue;
  MaterialStateFromJSON(Map<String, dynamic>? jsonDictValue,
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
  T? resolve(Set<MaterialState> states) {
    //debugPrint("MaterialStateFromJSON states: $states, _states: $_states");
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
