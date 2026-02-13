import 'package:flutter/material.dart';

import '../models/control.dart';
import 'enums.dart';
import 'numbers.dart';

MainAxisAlignment? parseMainAxisAlignment(String? value,
    [MainAxisAlignment? defaultValue]) {
  return parseEnum(MainAxisAlignment.values, value, defaultValue);
}

CrossAxisAlignment? parseCrossAxisAlignment(String? value,
    [CrossAxisAlignment? defaultValue]) {
  return parseEnum(CrossAxisAlignment.values, value, defaultValue);
}

TabAlignment? parseTabAlignment(String? value, [TabAlignment? defaultValue]) {
  return parseEnum(TabAlignment.values, value, defaultValue);
}

WrapAlignment? parseWrapAlignment(String? value,
    [WrapAlignment? defaultValue]) {
  return parseEnum(WrapAlignment.values, value, defaultValue);
}

WrapCrossAlignment? parseWrapCrossAlignment(String? value,
    [WrapCrossAlignment? defaultValue]) {
  return parseEnum(WrapCrossAlignment.values, value, defaultValue);
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
