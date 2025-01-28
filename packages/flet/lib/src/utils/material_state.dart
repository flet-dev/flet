import 'dart:collection';
import 'package:flutter/material.dart';

WidgetStateProperty<T?>? getWidgetStateProperty<T>(
    dynamic jsonDictValue, T Function(dynamic) converterFromJson,
    [T? defaultValue]) {
  if (jsonDictValue == null) {
    return null;
  }
  var j = jsonDictValue;
  if (j is! Map<String, dynamic>) {
    j = {"default": j};
  }
  return WidgetStateFromJSON(j, converterFromJson, defaultValue);
}

class WidgetStateFromJSON<T> extends WidgetStateProperty<T?> {
  late final LinkedHashMap<String, T> _states;
  late final T? _defaultValue;

  WidgetStateFromJSON(Map<String, dynamic>? jsonDictValue,
      T Function(dynamic) converterFromJson, T? defaultValue) {
    _defaultValue = defaultValue;

    // preserve user-defined order
    _states = LinkedHashMap<String, T>.from(
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
  T? resolve(Set<WidgetState> states) {
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
