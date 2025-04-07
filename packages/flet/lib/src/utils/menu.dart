import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'borders.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'material_state.dart';
import 'mouse.dart';
import 'numbers.dart';

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
    MenuStyle? defaultValue}) {
  if (value == null) return defaultValue;

  return MenuStyle(
    alignment: parseAlignment(value["alignment"], defaultAlignment)!,
    backgroundColor: parseWidgetStateColor(value["bgcolor"], theme,
        defaultColor: defaultBackgroundColor),
    shadowColor: parseWidgetStateColor(value["shadow_color"], theme,
        defaultColor: defaultShadowColor),
    surfaceTintColor: parseWidgetStateColor(value["surface_tint_color"], theme,
        defaultColor: defaultSurfaceTintColor),
    elevation: parseWidgetStateDouble(value["elevation"],
        defaultDouble: defaultElevation),
    padding: getWidgetStateProperty<EdgeInsetsGeometry?>(
        value["padding"], (jv) => parseEdgeInsets(jv), defaultPadding),
    side: getWidgetStateProperty<BorderSide?>(
        value["side"],
        (jv) => parseBorderSide(jv, theme,
            defaultSideColor: theme.colorScheme.outline),
        defaultBorderSide),
    shape: getWidgetStateProperty<OutlinedBorder?>(
        value["shape"], (jv) => parseOutlinedBorder(jv), defaultShape),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"],
        defaultMouseCursor: defaultMouseCursor),
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