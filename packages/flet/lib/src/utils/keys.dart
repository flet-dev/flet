import 'package:flutter/foundation.dart';

import '../models/control.dart';

abstract class ControlKey {
  final Object value;

  const ControlKey(this.value)
      : assert(
            value is int || value is String || value is bool || value is double,
            'Key value value must be int, String, bool, or double');

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other.runtimeType == runtimeType &&
          other is ControlKey &&
          other.value == value;

  @override
  int get hashCode => value.hashCode;

  @override
  String toString() => value.toString();
}

class ControlScrollKey extends ControlKey {
  const ControlScrollKey(super.value);
}

class ControlValueKey extends ControlKey {
  const ControlValueKey(super.value);
}

/// Preserves the value type because ValueKey equality is runtimeType-strict.
Key valueKeyFromValue(Object value) => switch (value) {
      String v => ValueKey<String>(v),
      int v => ValueKey<int>(v),
      double v => ValueKey<double>(v),
      bool v => ValueKey<bool>(v),
      _ => ValueKey(value),
    };

ControlKey? parseKey(dynamic value) {
  if (value == null) return null;

  if (value is Map) {
    var type = value["_type"];
    if (type == "value") {
      return ControlValueKey(value["value"]);
    } else if (type == "scroll") {
      return ControlScrollKey(value["value"]);
    }
    throw Exception("Unknown key type: $type");
  } else {
    return ControlValueKey(value);
  }
}

extension KeysParsers on Control {
  ControlKey? getKey(String propertyName) {
    return parseKey(get(propertyName));
  }
}
