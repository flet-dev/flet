import 'dart:convert';

import 'package:flet/src/utils/transforms.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'borders.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'material_state.dart';
import 'mouse.dart';
import 'numbers.dart';
import 'text.dart';
import 'theme.dart';

ButtonStyle? parseButtonStyle(ThemeData theme, Control control, String propName,
    {Color? defaultForegroundColor,
    Color? defaultBackgroundColor,
    Color? defaultOverlayColor,
    Color? defaultShadowColor,
    Color? defaultSurfaceTintColor,
    double? defaultElevation,
    EdgeInsets? defaultPadding,
    BorderSide? defaultBorderSide,
    OutlinedBorder? defaultShape}) {
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

ButtonStyle? buttonStyleFromJSON(ThemeData theme, Map<String, dynamic>? json,
    [Color? defaultForegroundColor,
    Color? defaultBackgroundColor,
    Color? defaultOverlayColor,
    Color? defaultShadowColor,
    Color? defaultSurfaceTintColor,
    double? defaultElevation,
    EdgeInsets? defaultPadding,
    BorderSide? defaultBorderSide,
    OutlinedBorder? defaultShape]) {
  if (json == null) {
    return null;
  }
  return ButtonStyle(
    foregroundColor: getWidgetStateProperty<Color?>(json["color"],
        (jv) => parseColor(theme, jv as String), defaultForegroundColor),
    backgroundColor: getWidgetStateProperty<Color?>(json["bgcolor"],
        (jv) => parseColor(theme, jv as String), defaultBackgroundColor),
    overlayColor: getWidgetStateProperty<Color?>(json["overlay_color"],
        (jv) => parseColor(theme, jv as String), defaultOverlayColor),
    shadowColor: getWidgetStateProperty<Color?>(json["shadow_color"],
        (jv) => parseColor(theme, jv as String), defaultShadowColor),
    surfaceTintColor: getWidgetStateProperty<Color?>(json["surface_tint_color"],
        (jv) => parseColor(theme, jv as String), defaultSurfaceTintColor),
    elevation: getWidgetStateProperty(
        json["elevation"], (jv) => parseDouble(jv, 0)!, defaultElevation),
    animationDuration: json["animation_duration"] != null
        ? Duration(milliseconds: parseInt(json["animation_duration"], 0)!)
        : null,
    padding: getWidgetStateProperty<EdgeInsetsGeometry?>(
        json["padding"], (jv) => edgeInsetsFromJson(jv), defaultPadding),
    side: getWidgetStateProperty<BorderSide?>(
        json["side"],
        (jv) => borderSideFromJSON(theme, jv, theme.colorScheme.outline),
        defaultBorderSide),
    shape: getWidgetStateProperty<OutlinedBorder?>(
        json["shape"], (jv) => outlinedBorderFromJSON(jv), defaultShape),
    iconColor: getWidgetStateProperty<Color?>(json["icon_color"],
        (jv) => parseColor(theme, jv as String), defaultForegroundColor),
    alignment: alignmentFromJson(json["alignment"]),
    enableFeedback: parseBool(json["enable_feedback"]),
    textStyle: getWidgetStateProperty<TextStyle?>(
        json["text_style"], (jv) => textStyleFromJson(theme, jv)),
    iconSize: getWidgetStateProperty<double?>(
        json["icon_size"], (jv) => parseDouble(jv)),
    visualDensity: parseVisualDensity(json["visual_density"]),
    mouseCursor: getWidgetStateProperty<MouseCursor?>(
        json["mouse_cursor"], (jv) => parseMouseCursor(jv)),
  );
}

FloatingActionButtonLocation? parseFloatingActionButtonLocation(
    Control control, String propName, [FloatingActionButtonLocation? defValue]) {
  const Map<String, FloatingActionButtonLocation> fabLocations = {
    "centerdocked": FloatingActionButtonLocation.centerDocked,
    "centerfloat": FloatingActionButtonLocation.centerFloat,
    "centertop": FloatingActionButtonLocation.centerTop,
    "endcontained": FloatingActionButtonLocation.endContained,
    "enddocked": FloatingActionButtonLocation.endDocked,
    "endfloat": FloatingActionButtonLocation.endFloat,
    "endtop": FloatingActionButtonLocation.endTop,
    "minicenterdocked": FloatingActionButtonLocation.miniCenterDocked,
    "minicenterfloat": FloatingActionButtonLocation.miniCenterFloat,
    "minicentertop": FloatingActionButtonLocation.miniCenterTop,
    "miniendfloat": FloatingActionButtonLocation.miniEndFloat,
    "miniendtop": FloatingActionButtonLocation.miniEndTop,
    "ministartdocked": FloatingActionButtonLocation.miniStartDocked,
    "ministartfloat": FloatingActionButtonLocation.miniStartFloat,
    "ministarttop": FloatingActionButtonLocation.miniStartTop,
    "startdocked": FloatingActionButtonLocation.startDocked,
    "startfloat": FloatingActionButtonLocation.startFloat,
    "starttop": FloatingActionButtonLocation.startTop
  };

  try {
    var fabLocationOffset = parseOffset(control, propName);
    if (fabLocationOffset != null) {
      return CustomFloatingActionButtonLocation(
          dx: fabLocationOffset.dx, dy: fabLocationOffset.dy);
    } else {
      return defValue;
    }
  } catch (e) {
    var key = control.attrString(propName, "")!.toLowerCase();
    return fabLocations.containsKey(key) ? fabLocations[key]! : defValue;
  }
}

class CustomFloatingActionButtonLocation extends FloatingActionButtonLocation {
  final double dx;
  final double dy;

  CustomFloatingActionButtonLocation({required this.dx, required this.dy});

  @override
  Offset getOffset(ScaffoldPrelayoutGeometry scaffoldGeometry) {
    return Offset(scaffoldGeometry.scaffoldSize.width - dx,
        scaffoldGeometry.scaffoldSize.height - dy);
  }

  @override
  bool operator ==(Object other) =>
      other is CustomFloatingActionButtonLocation &&
      other.dx == dx &&
      other.dy == dy;

  @override
  int get hashCode => dx.hashCode + dy.hashCode;

  @override
  String toString() => 'CustomFloatingActionButtonLocation(dx: $dx, dy: $dy)';
}
