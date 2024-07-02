import 'dart:convert';

import 'package:flet/src/utils/transforms.dart';
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
      surfaceTintColor: getWidgetStateProperty<Color?>(
          json["surface_tint_color"],
          (jv) => parseColor(theme, jv as String),
          defaultSurfaceTintColor),
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
          json["shape"], (jv) => outlinedBorderFromJSON(jv), defaultShape));
}

FloatingActionButtonLocation parseFloatingActionButtonLocation(
    Control control, String propName, FloatingActionButtonLocation defValue) {
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
    OffsetDetails? fabLocationOffsetDetails = parseOffset(control, propName);
    if (fabLocationOffsetDetails != null) {
      return CustomFloatingActionButtonLocation(
          dx: fabLocationOffsetDetails.x, dy: fabLocationOffsetDetails.y);
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
