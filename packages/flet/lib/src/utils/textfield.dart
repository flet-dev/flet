import 'package:flutter/services.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

FilteringTextInputFormatter? parseInputFilter(dynamic value,
    [FilteringTextInputFormatter? defaultValue]) {
  if (value == null) return defaultValue;
  var regexString = value["regex_string"]?.toString();
  if (regexString == null) return defaultValue;
  return CustomFilteringTextInputFormatter.fromJSON(value);
}
class CustomFilteringTextInputFormatter extends FilteringTextInputFormatter {
  final RegExp _pattern;

  CustomFilteringTextInputFormatter._(this._pattern,
      {bool allow = true, String replacementString = ""})
      : super(_pattern, allow: allow, replacementString: replacementString);

  // Factory constructor to create an instance from JSON
  factory CustomFilteringTextInputFormatter.fromJSON(
      Map<String, dynamic> json) {
    final pattern = RegExp(
      json["regex_string"]?.toString() ?? "",
      multiLine: parseBool(json["multiline"], false)!,
      unicode: parseBool(json["unicode"], false)!,
      caseSensitive: parseBool(json["case_sensitive"], true)!,
      dotAll: parseBool(json["dot_all"], false)!,
    );

    return CustomFilteringTextInputFormatter._(pattern,
        allow: parseBool(json["allow"], true)!,
        replacementString: json["replacement_string"]?.toString() ?? "");
  }

  @override
  TextEditingValue formatEditUpdate(
      TextEditingValue oldValue, TextEditingValue newValue) {
    // Check if the new value matches the regex pattern and return it if it does
    if (_pattern.hasMatch(newValue.text)) {
      return newValue;
    }
    return oldValue;
  }
}

extension InputFormatterParsers on Control {
  FilteringTextInputFormatter? getTextInputFormatter(String propertyName,
      [FilteringTextInputFormatter? defaultValue]) {
    return parseInputFilter(get(propertyName), defaultValue);
  }
}
