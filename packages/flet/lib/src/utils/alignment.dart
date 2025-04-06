
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import 'numbers.dart';

MainAxisAlignment? parseMainAxisAlignment(String? value,
    [MainAxisAlignment? defaultValue]) {
  if (value == null) return defaultValue;

  return MainAxisAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

CrossAxisAlignment? parseCrossAxisAlignment(String? value,
    [CrossAxisAlignment? defaultValue]) {
  if (value == null) return defaultValue;

  return CrossAxisAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TabAlignment? parseTabAlignment(String? value, [TabAlignment? defaultValue]) {
  if (value == null) return defaultValue;

  return TabAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

WrapAlignment? parseWrapAlignment(String? value,
    [WrapAlignment? defaultValue]) {
  if (value == null) return defaultValue;

  return WrapAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

WrapCrossAlignment? parseWrapCrossAlignment(String? value,
    [WrapCrossAlignment? defaultValue]) {
  if (value == null) return defaultValue;

  return WrapCrossAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Alignment? parseAlignment(dynamic value, [Alignment? defaultValue]) {
  if (value == null) return defaultValue;
  return Alignment(parseDouble(value['x'], 0)!, parseDouble(value['y'], 0)!);
}
