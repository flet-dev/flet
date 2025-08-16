import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import 'material_state.dart';

IconData? parseIconData(int? value, FletBackend backend,
    [IconData? defaultValue]) {
  if (value == null) return defaultValue;

  for (var extension in backend.extensions) {
    var iconData = extension.createIconData(value);
    if (iconData != null) {
      return iconData;
    }
  }

  return defaultValue;
}

WidgetStateProperty<Icon?>? parseWidgetStateIcon(
  dynamic value,
  FletBackend backend,
  ThemeData theme, {
  Icon? defaultIcon,
  WidgetStateProperty<Icon?>? defaultValue,
}) {
  if (value == null) return defaultValue;
  return getWidgetStateProperty<Icon?>(
      value, (jv) => Icon(parseIconData(jv as int, backend)), defaultIcon);
}

extension IconParsers on Control {
  IconData? getIconData(String propertyName, [IconData? defaultValue]) {
    return parseIconData(get(propertyName), backend, defaultValue);
  }

  WidgetStateProperty<Icon?>? getWidgetStateIcon(
      String propertyName, ThemeData theme,
      {Icon? defaultIcon, WidgetStateProperty<Icon?>? defaultValue}) {
    return parseWidgetStateIcon(get(propertyName), backend, theme,
        defaultIcon: defaultIcon, defaultValue: defaultValue);
  }
}
