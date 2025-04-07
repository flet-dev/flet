import 'package:flutter/material.dart';

import '../models/control.dart';
import 'cupertino_icons.dart';
import 'material_icons.dart';
import 'material_state.dart';

IconData? parseIcon(String? value, [IconData? defaultValue]) {
  if (value == null) return defaultValue;
  return materialIcons[value.toLowerCase()] ??
      cupertinoIcons[value.toLowerCase()];
}

WidgetStateProperty<Icon?>? parseWidgetStateIcon(dynamic value,
    ThemeData theme, {
      Icon? defaultIcon,
      WidgetStateProperty<Icon?>? defaultValue,
    }) {
  if (value == null) return defaultValue;
  return getWidgetStateProperty<Icon?>(
      value, (jv) => Icon(parseIcon(jv as String)), defaultIcon);
}

extension IconParsers on Control {
  IconData? getIcon(String propertyName, [IconData? defaultValue]) {
    return parseIcon(get(propertyName), defaultValue);
  }

  WidgetStateProperty<Icon?>? getWidgetStateIcon(
      String propertyName, ThemeData theme,
      {Icon? defaultIcon, WidgetStateProperty<Icon?>? defaultValue}) {
    return parseWidgetStateIcon(get(propertyName), theme,
        defaultIcon: defaultIcon, defaultValue: defaultValue);
  }
}
