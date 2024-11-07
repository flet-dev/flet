import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'borders.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'material_state.dart';
import 'mouse.dart';
import 'numbers.dart';

MenuStyle? parseMenuStyle(ThemeData theme, Control control, String propName,
    {Color? defaultBackgroundColor,
    Color? defaultShadowColor,
    Color? defaultSurfaceTintColor,
    double? defaultElevation,
    Alignment? defaultAlignment,
    MouseCursor? defaultMouseCursor,
    EdgeInsets? defaultPadding,
    BorderSide? defaultBorderSide,
    OutlinedBorder? defaultShape}) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return menuStyleFromJSON(
      theme,
      j1,
      defaultBackgroundColor,
      defaultShadowColor,
      defaultSurfaceTintColor,
      defaultElevation,
      defaultAlignment,
      defaultMouseCursor,
      defaultPadding,
      defaultBorderSide,
      defaultShape);
}

MenuStyle? menuStyleFromJSON(ThemeData theme, Map<String, dynamic>? json,
    [Color? defaultBackgroundColor,
    Color? defaultShadowColor,
    Color? defaultSurfaceTintColor,
    double? defaultElevation,
    Alignment? defaultAlignment,
    MouseCursor? defaultMouseCursor,
    EdgeInsets? defaultPadding,
    BorderSide? defaultBorderSide,
    OutlinedBorder? defaultShape]) {
  if (json == null) {
    return null;
  }
  return MenuStyle(
    alignment: alignmentFromJson(json["alignment"], defaultAlignment)!,
    backgroundColor: getWidgetStateProperty<Color?>(json["bgcolor"],
        (jv) => parseColor(theme, jv as String), defaultBackgroundColor),
    shadowColor: getWidgetStateProperty<Color?>(json["shadow_color"],
        (jv) => parseColor(theme, jv as String), defaultShadowColor),
    surfaceTintColor: getWidgetStateProperty<Color?>(json["surface_tint_color"],
        (jv) => parseColor(theme, jv as String), defaultSurfaceTintColor),
    elevation: getWidgetStateProperty<double?>(
        json["elevation"], (jv) => parseDouble(jv, 0)!, defaultElevation),
    padding: getWidgetStateProperty<EdgeInsetsGeometry?>(
        json["padding"], (jv) => edgeInsetsFromJson(jv), defaultPadding),
    side: getWidgetStateProperty<BorderSide?>(
        json["side"],
        (jv) => borderSideFromJSON(theme, jv, theme.colorScheme.outline),
        defaultBorderSide),
    shape: getWidgetStateProperty<OutlinedBorder?>(
        json["shape"], (jv) => outlinedBorderFromJSON(jv), defaultShape),
    mouseCursor: getWidgetStateProperty<MouseCursor?>(json["mouse_cursor"],
        (jv) => parseMouseCursor(jv as String), defaultMouseCursor),
  );
}
