import 'dart:convert';

import '../models/control.dart';

List<String>? parseStringList(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final jv = json.decode(v);
  return (jv as List).map((c) => c as String).toList();
}

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
