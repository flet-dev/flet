import 'dart:convert';

import 'package:flutter/services.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

FilteringTextInputFormatter? parseInputFilter(
    Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return inputFilterFromJSON(j1);
}

FilteringTextInputFormatter inputFilterFromJSON(dynamic json) {
  bool allow = true;
  String? regexString = "";
  String? replacementString = "";

  if (json != null) {
    allow = parseBool(json["allow"], true)!;
    regexString = json["regex_string"]?.toString();
    replacementString = json["replacement_string"]?.toString();
  }

  return FilteringTextInputFormatter(RegExp(regexString ?? ""),
      allow: allow, replacementString: replacementString ?? "");
}
