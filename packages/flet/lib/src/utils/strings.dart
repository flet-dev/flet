String trimStart(String str, String symbol) {
  if (str.startsWith(symbol)) {
    return str.substring(symbol.length);
  } else {
    return str;
  }
}

String trimEnd(String str, String symbol) {
  if (str.endsWith(symbol)) {
    return str.substring(0, str.length - symbol.length);
  } else {
    return str;
  }
}

String trim(String str, String symbol) {
  return trimEnd(trimStart(str, symbol), symbol);
}
