import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/theme.dart';
import 'alignment.dart';
import 'borders.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'geometry.dart';
import 'mouse.dart';
import 'numbers.dart';
import 'widget_state.dart';

MenuStyle? parseMenuStyle(dynamic value, ThemeData theme,
    {Color? defaultBackgroundColor,
    Color? defaultShadowColor,
    Color? defaultSurfaceTintColor,
    double? defaultElevation,
    Alignment? defaultAlignment,
    MouseCursor? defaultMouseCursor,
    EdgeInsets? defaultPadding,
    BorderSide? defaultBorderSide,
    OutlinedBorder? defaultShape,
    Size? defaultMinimumSize,
    Size? defaultMaximumSize,
    Size? defaultFixedSize,
    VisualDensity? defaultVisualDensity,
    MenuStyle? defaultValue}) {
  if (value == null) return defaultValue;

  return MenuStyle(
    alignment: parseAlignment(value["alignment"], defaultAlignment),
    backgroundColor: parseWidgetStateColor(value["bgcolor"], theme,
        defaultColor: defaultBackgroundColor),
    shadowColor: parseWidgetStateColor(value["shadow_color"], theme,
        defaultColor: defaultShadowColor),
    elevation: parseWidgetStateDouble(value["elevation"],
        defaultDouble: defaultElevation),
    padding: getWidgetStateProperty<EdgeInsetsGeometry?>(
        value["padding"], (jv) => parseEdgeInsets(jv), defaultPadding),
    side: getWidgetStateProperty<BorderSide?>(
        value["side"],
        (jv) => parseBorderSide(jv, theme,
            defaultSideColor: theme.colorScheme.outline),
        defaultBorderSide),
    shape: parseWidgetStateOutlinedBorder(value["shape"], theme,
        defaultOutlinedBorder: defaultShape),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"],
        defaultMouseCursor: defaultMouseCursor),
    minimumSize: parseWidgetStateSize(value["min_size"],
        defaultSize: defaultMinimumSize),
    maximumSize: parseWidgetStateSize(value["max_size"],
        defaultSize: defaultMaximumSize),
    fixedSize: parseWidgetStateSize(value["fixed_size"],
        defaultSize: defaultFixedSize),
    visualDensity:
        parseVisualDensity(value["visual_density"], defaultVisualDensity),
  );
}

extension MenuParsers on Control {
  MenuStyle? getMenuStyle(String propertyName, ThemeData theme,
      {Color? defaultBackgroundColor,
      Color? defaultShadowColor,
      Color? defaultSurfaceTintColor,
      double? defaultElevation,
      Alignment? defaultAlignment,
      MouseCursor? defaultMouseCursor,
      EdgeInsets? defaultPadding,
      BorderSide? defaultBorderSide,
      OutlinedBorder? defaultShape,
      MenuStyle? defaultValue}) {
    return parseMenuStyle(get(propertyName), theme,
        defaultBackgroundColor: defaultBackgroundColor,
        defaultShadowColor: defaultShadowColor,
        defaultSurfaceTintColor: defaultSurfaceTintColor,
        defaultElevation: defaultElevation,
        defaultAlignment: defaultAlignment,
        defaultMouseCursor: defaultMouseCursor,
        defaultPadding: defaultPadding,
        defaultBorderSide: defaultBorderSide,
        defaultShape: defaultShape,
        defaultValue: defaultValue);
  }
}
