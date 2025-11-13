import 'dart:convert';

extension StringExtension on String {
  /// Trims the [symbol] from the start of the string.
  String trimStart(String symbol) {
    return startsWith(symbol) ? substring(symbol.length) : this;
  }

  /// Trims the [symbol] from the end of the string.
  String trimEnd(String symbol) {
    return endsWith(symbol) ? substring(0, length - symbol.length) : this;
  }

  /// Trims the [symbol] from both the start and end of the string.
  String trimSymbol(String symbol) {
    return trimStart(symbol).trimEnd(symbol);
  }

  /// Returns `true` if the string contains valid Base64-encoded data.
  ///
  /// The string is first cleaned (data URI prefixes removed, whitespace
  /// stripped) and then normalized using [base64.normalize], which validates
  /// characters, fixes padding, and ensures proper length.
  ///
  /// If normalization and subsequent decoding via [base64.decode] both
  /// succeed, the string is considered valid Base64.
  bool get isBase64 {
    var s = stripBase64DataHeader().replaceAll(RegExp(r'\s+'), '');

    try {
      final normalized = base64.normalize(s);
      base64.decode(normalized);
      return true;
    } catch (_) {
      return false;
    }
  }

  /// Removes a leading Base64 data URI header (e.g. `data:*;base64,`)
  /// if present, and returns only the Base64 payload.
  String stripBase64DataHeader() {
    var s = this;
    if (s.startsWith('data:')) {
      final comma = s.indexOf(',');
      if (comma != -1) {
        return s.substring(comma + 1);
      }
    }
    return s;
  }
}
