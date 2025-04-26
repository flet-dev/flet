import 'package:flutter/foundation.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

Map<String, double>? parseResponsiveNumber(dynamic value, double defaultValue) {
  Map<String, double> result = {};

  if (value != null) {
    if (value is Map) {
      result = value.map<String, double>(
        (key, val) => MapEntry(key.toString(), parseDouble(val, 0)!),
      );
    } else {
      result[""] = value;
    }
  }

  if (result[""] == null) {
    result[""] = defaultValue;
  }

  return result;
}

double getBreakpointNumber(
    Map<String, double> value, double width, Map<String, double> breakpoints) {
  // default value
  double? result = value[""];

  debugPrint("getBreakpointNumber: $value, $width, $breakpoints");

  double maxBpWidth = 0;
  value.forEach((bpName, respValue) {
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
    throw Exception("Responsive number not found for width=$width: $value");
  }
  return result!;
}

extension ResponsiveParsers on Control {
  Map<String, double>? getResponsiveNumber(
      String propertyName, double defaultValue) {
    return parseResponsiveNumber(get(propertyName), defaultValue);
  }
}
