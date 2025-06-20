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
}
