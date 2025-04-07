import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

DismissDirection? parseDismissDirection(String? value,
    [DismissDirection? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return DismissDirection.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Map<DismissDirection, double>? parseDismissThresholds(dynamic value,
    [Map<DismissDirection, double>? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is! Map<String, dynamic>) {
    value = {"": value};
  }

  Map<DismissDirection, double> dismissDirectionMap = {};
  value.forEach((directionStr, jv) {
    directionStr.split(",").map((s) => s.trim().toLowerCase()).forEach((state) {
      DismissDirection d = parseDismissDirection(state, DismissDirection.none)!;
      if (d != DismissDirection.none) {
        dismissDirectionMap[d] = parseDouble(jv, 0)!;
      }
    });
  });

  return dismissDirectionMap;
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