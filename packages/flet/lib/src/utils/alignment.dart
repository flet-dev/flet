
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
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

extension AlignmentParsers on Control {
  MainAxisAlignment? getMainAxisAlignment(String propertyName,
      [MainAxisAlignment? defaultValue]) {
    return parseMainAxisAlignment(get(propertyName), defaultValue);
  }

  CrossAxisAlignment? getCrossAxisAlignment(String propertyName,
      [CrossAxisAlignment? defaultValue]) {
    return parseCrossAxisAlignment(get(propertyName), defaultValue);
  }

  TabAlignment? getTabAlignment(String propertyName,
      [TabAlignment? defaultValue]) {
    return parseTabAlignment(get(propertyName), defaultValue);
  }

  WrapAlignment? getWrapAlignment(String propertyName,
      [WrapAlignment? defaultValue]) {
    return parseWrapAlignment(get(propertyName), defaultValue);
  }

  WrapCrossAlignment? getWrapCrossAlignment(String propertyName,
      [WrapCrossAlignment? defaultValue]) {
    return parseWrapCrossAlignment(get(propertyName), defaultValue);
  }

  Alignment? getAlignment(String propertyName, [Alignment? defaultValue]) {
    return parseAlignment(get(propertyName), defaultValue);
  }
}