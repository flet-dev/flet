import 'package:flutter/services.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

FilteringTextInputFormatter? parseInputFilter(dynamic value,
    [FilteringTextInputFormatter? defaultValue]) {
  if (value == null) return defaultValue;
  var regexString = value["regex_string"]?.toString();
  if (regexString == null) return defaultValue;
  return CustomFilteringTextInputFormatter.fromMap(value);
}

class CustomFilteringTextInputFormatter extends FilteringTextInputFormatter {
  final RegExp _pattern;

  CustomFilteringTextInputFormatter._(this._pattern,
      {bool allow = true, String replacementString = ""})
      : super(_pattern, allow: allow, replacementString: replacementString);

  // Factory constructor to create an instance from a map
  factory CustomFilteringTextInputFormatter.fromMap(
      Map<dynamic, dynamic> value) {
    final pattern = RegExp(
      value["regex_string"]?.toString() ?? "",
      multiLine: parseBool(value["multiline"], false)!,
      unicode: parseBool(value["unicode"], false)!,
      caseSensitive: parseBool(value["case_sensitive"], true)!,
      dotAll: parseBool(value["dot_all"], false)!,
    );

    return CustomFilteringTextInputFormatter._(pattern,
        allow: parseBool(value["allow"], true)!,
        replacementString: value["replacement_string"]?.toString() ?? "");
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

class TextCapitalizationFormatter extends TextInputFormatter {
  final TextCapitalization capitalization;

  TextCapitalizationFormatter(this.capitalization);

  @override
  TextEditingValue formatEditUpdate(
      TextEditingValue oldValue, TextEditingValue newValue) {
    String text = '';

    switch (capitalization) {
      case TextCapitalization.words:
        text = capitalizeFirstofEach(newValue.text);
        break;
      case TextCapitalization.sentences:
        List<String> sentences = newValue.text.split('.');
        for (int i = 0; i < sentences.length; i++) {
          sentences[i] = inCaps(sentences[i]);
        }
        text = sentences.join('.');
        break;
      case TextCapitalization.characters:
        text = allInCaps(newValue.text);
        break;
      case TextCapitalization.none:
        text = newValue.text;
        break;
    }

    return TextEditingValue(
      text: text,
      selection: newValue.selection,
    );
  }

  /// 'Hello world'
  static String inCaps(String text) {
    if (text.isEmpty) {
      return text;
    }
    String result = '';
    for (int i = 0; i < text.length; i++) {
      if (text[i] != ' ') {
        result += '${text[i].toUpperCase()}${text.substring(i + 1)}';
        break;
      } else {
        result += text[i];
      }
    }
    return result;
  }

  /// 'HELLO WORLD'
  static String allInCaps(String text) => text.toUpperCase();

  /// 'Hello World'
  static String capitalizeFirstofEach(String text) => text
      .replaceAll(RegExp(' +'), ' ')
      .split(" ")
      .map((str) => inCaps(str))
      .join(" ");
}

class CustomNumberFormatter extends TextInputFormatter {
  final String pattern;

  CustomNumberFormatter(this.pattern);

  @override
  TextEditingValue formatEditUpdate(
      TextEditingValue oldValue, TextEditingValue newValue) {
    final regExp = RegExp(pattern);
    if (regExp.hasMatch(newValue.text)) {
      return newValue;
    }
    // If newValue is invalid, keep the old value
    return oldValue;
  }
}

extension InputFormatterParsers on Control {
  FilteringTextInputFormatter? getTextInputFormatter(String propertyName,
      [FilteringTextInputFormatter? defaultValue]) {
    return parseInputFilter(get(propertyName), defaultValue);
  }
}
