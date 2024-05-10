import 'dart:convert';

import '../models/control.dart';
import '../utils/numbers.dart';

Map<String, double> parseResponsiveNumber(
    Control control, String propName, double defaultValue) {
  var v = control.attrString(propName, null);
  Map<String, double> result = {};
  if (v != null) {
    var j = json.decode(v);
    if (j is! Map<String, dynamic>) {
      j = {"": j};
    }
    result = responsiveNumberFromJson(j);
  }
  if (result[""] == null) {
    result[""] = defaultValue;
  }
  return result;
}

Map<String, double> responsiveNumberFromJson(Map<String, dynamic> json) {
  return json.map((key, value) => MapEntry(key, parseDouble(value, 0)!));
}

double getBreakpointNumber(Map<String, double> responsiveNumber, double width,
    Map<String, double> breakpoints) {
  // default value
  double? result = responsiveNumber[""];

  double maxBpWidth = 0;
  responsiveNumber.forEach((bpName, respValue) {
    if (bpName == "") {
      return;
    }
    var bpWidth = breakpoints[bpName];
    if (bpWidth == null) {
      throw Exception("Unknown breakpoint: $bpName");
    }
    if (width >= bpWidth && bpWidth >= maxBpWidth) {
      maxBpWidth = bpWidth;
      result = respValue;
    }
  });

  if (result == null) {
    throw Exception(
        "Responsive number not found for width=$width: $responsiveNumber");
  }
  return result!;
}
