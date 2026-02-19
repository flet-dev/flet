import 'package:flutter/material.dart';
import 'enums.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

DismissDirection? parseDismissDirection(String? value,
    [DismissDirection? defaultValue]) {
  return parseEnum(DismissDirection.values, value, defaultValue);
}

Map<DismissDirection, double>? parseDismissThresholds(dynamic value,
    [Map<DismissDirection, double>? defaultValue]) {
  if (value == null) return defaultValue;

  Map<DismissDirection, double> result = {};
  value.forEach((d, t) {
    var direction = parseDismissDirection(d, DismissDirection.none)!;
    if (direction != DismissDirection.none) {
      var threshold = parseDouble(t, 0.0)!;
      result[direction] = threshold;
    }
  });

  return result;
}

extension DismissibleParsers on Control {
  DismissDirection? getDismissDirection(String propertyName,
      [DismissDirection? defaultValue]) {
    return parseDismissDirection(get(propertyName), defaultValue);
  }

  Map<DismissDirection, double>? getDismissThresholds(String propertyName,
      [Map<DismissDirection, double>? defaultValue]) {
    return parseDismissThresholds(get(propertyName), defaultValue);
  }
}
