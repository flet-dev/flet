import 'package:flutter/material.dart';

@immutable
class AutoCompleteSuggestion {
  const AutoCompleteSuggestion({
    required this.key,
    required this.value,
  });

  final String key;
  final String value;

  @override
  String toString() {
    return value;
  }

  String selectionString() {
    return key;
  }

  Map<String, dynamic> toMap() => <String, dynamic>{'key': key, 'value': value};

  @override
  bool operator ==(Object other) {
    if (other.runtimeType != runtimeType) {
      return false;
    }
    return other is AutoCompleteSuggestion &&
        other.key == key &&
        other.value == value;
  }

  @override
  int get hashCode => Object.hash(key, value);
}

List<AutoCompleteSuggestion>? parseAutoCompleteSuggestions(
  dynamic value, [
  List<AutoCompleteSuggestion>? defaultValue,
]) {
  if (value == null) return defaultValue;

  List<AutoCompleteSuggestion> m = [];

  if (value is List) {
    for (var json in value) {
      var key = json["key"];
      var val = json["value"];

      if ((key == null || key.toString().isEmpty) &&
          (val == null || val.toString().isEmpty)) {
        continue;
      }

      key ??= val;
      val ??= key;

      m.add(AutoCompleteSuggestion(
        key: key.toString(),
        value: val.toString(),
      ));
    }
  }

  return m;
}