import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'borders.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'material_state.dart';
import 'numbers.dart';

ButtonStyle? parseButtonStyle(ThemeData theme, Control control, String propName,
    {required Color defaultForegroundColor,
    required Color defaultBackgroundColor,
    required Color defaultOverlayColor,
    required Color defaultShadowColor,
    required Color defaultSurfaceTintColor,
    required double defaultElevation,
    required EdgeInsets defaultPadding,
    required BorderSide defaultBorderSide,
    required OutlinedBorder defaultShape}) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return buttonStyleFromJSON(
      theme,
      j1,
      defaultForegroundColor,
      defaultBackgroundColor,
      defaultOverlayColor,
      defaultShadowColor,
      defaultSurfaceTintColor,
      defaultElevation,
      defaultPadding,
      defaultBorderSide,
      defaultShape);
}

MaterialStateProperty<Color?>? parseMaterialStateColor(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return getMaterialStateProperty<Color?>(
      j1, (jv) => HexColor.fromString(theme, jv as String), null);
}

Color? parseMaterialStateColorForCupertino(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return getMaterialStateProperty<Color?>(
      j1, (jv) => HexColor.fromString(theme, jv as String), null);
}

ButtonStyle? buttonStyleFromJSON(
    ThemeData theme,
    Map<String, dynamic> json,
    Color defaultForegroundColor,
    Color defaultBackgroundColor,
    Color defaultOverlayColor,
    Color defaultShadowColor,
    Color defaultSurfaceTintColor,
    double defaultElevation,
    EdgeInsets defaultPadding,
    BorderSide defaultBorderSide,
    OutlinedBorder defaultShape) {
  return ButtonStyle(
      foregroundColor: getMaterialStateProperty<Color?>(
          json["color"],
          (jv) => HexColor.fromString(theme, jv as String),
          defaultForegroundColor),
      backgroundColor: getMaterialStateProperty<Color?>(
          json["bgcolor"],
          (jv) => HexColor.fromString(theme, jv as String),
          defaultBackgroundColor),
      overlayColor: getMaterialStateProperty<Color?>(
          json["overlay_color"],
          (jv) => HexColor.fromString(theme, jv as String),
          defaultOverlayColor),
      shadowColor: getMaterialStateProperty<Color?>(json["shadow_color"],
          (jv) => HexColor.fromString(theme, jv as String), defaultShadowColor),
      surfaceTintColor: getMaterialStateProperty<Color?>(
          json["surface_tint_color"],
          (jv) => HexColor.fromString(theme, jv as String),
          defaultSurfaceTintColor),
      elevation: getMaterialStateProperty(
          json["elevation"], (jv) => parseDouble(jv), defaultElevation),
      animationDuration: json["animation_duration"] != null
          ? Duration(milliseconds: parseInt(json["animation_duration"]))
          : null,
      padding: getMaterialStateProperty(
          json["padding"], (jv) => edgeInsetsFromJson(jv), defaultPadding),
      side: getMaterialStateProperty<BorderSide?>(
          json["side"],
          (jv) => borderSideFromJSON(theme, jv, theme.colorScheme.outline),
          defaultBorderSide),
      shape: getMaterialStateProperty<OutlinedBorder?>(
          json["shape"], (jv) => outlinedBorderFromJSON(jv), defaultShape));
}
