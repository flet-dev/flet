import 'package:flutter/material.dart';

import '../models/control.dart';
import 'material_state.dart';

IconData? parseIconData(int? value, [IconData? defaultValue]) {
  if (value == null) return defaultValue;

  int setId = (value >> 16) & 0xFF;
  int codePoint = value & 0xFFFF;
  String? fontFamily;
  String? fontPackage;

  if (setId == 1) {
    fontFamily = "MaterialIcons";
  } else if (setId == 2) {
    fontFamily = "CupertinoIcons";
    fontPackage = "cupertino_icons";
  }

  return IconData(codePoint, fontFamily: fontFamily, fontPackage: fontPackage);
}

WidgetStateProperty<Icon?>? parseWidgetStateIcon(
  dynamic value,
  ThemeData theme, {
  Icon? defaultIcon,
  WidgetStateProperty<Icon?>? defaultValue,
}) {
  if (value == null) return defaultValue;
  return getWidgetStateProperty<Icon?>(
      value, (jv) => Icon(parseIconData(jv as int)), defaultIcon);
}

extension IconParsers on Control {
  IconData? getIconData(String propertyName, [IconData? defaultValue]) {
    return parseIconData(get(propertyName), defaultValue);
  }

  WidgetStateProperty<Icon?>? getWidgetStateIcon(
      String propertyName, ThemeData theme,
      {Icon? defaultIcon, WidgetStateProperty<Icon?>? defaultValue}) {
    return parseWidgetStateIcon(get(propertyName), theme,
        defaultIcon: defaultIcon, defaultValue: defaultValue);
  }
}
