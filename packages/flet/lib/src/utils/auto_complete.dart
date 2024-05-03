import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';

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

  Map<String, dynamic> toJson() => <String, dynamic>{
        'key': key,
        'value': value,
      };

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

List<AutoCompleteSuggestion> parseAutoCompleteSuggestions(
    Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return [];
  }

  final j1 = json.decode(v);
  return autoCompleteSuggestionsFromJSON(j1);
}

List<AutoCompleteSuggestion> autoCompleteSuggestionsFromJSON(dynamic json) {
  List<AutoCompleteSuggestion> m = [];
  if (json is List) {
    json.map((e) => autoCompleteSuggestionFromJSON(e)).toList().forEach((e) {
      if (e != null) {
        m.add(e);
      }
    });
  }
  return m;
}

AutoCompleteSuggestion? autoCompleteSuggestionFromJSON(dynamic json) {
  var key = json["key"];
  var value = json["value"];
  if ((key == null || key.toString().isEmpty) &&
      (value == null || value.toString().isEmpty)) {
    return null;
  }
  if (key == null && value != null) {
    key = value;
  }
  if (value == null && key != null) {
    value = key;
  }
  return AutoCompleteSuggestion(
    key: key.toString(),
    value: value.toString(),
  );
}
