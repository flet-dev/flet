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

FloatingActionButtonLocation parseFloatingActionButtonLocation(
    Control control, String propName, FloatingActionButtonLocation defValue) {
  List<FloatingActionButtonLocation> fabLocations = [
    FloatingActionButtonLocation.centerDocked,
    FloatingActionButtonLocation.centerFloat,
    FloatingActionButtonLocation.centerTop,
    FloatingActionButtonLocation.endContained,
    FloatingActionButtonLocation.endDocked,
    FloatingActionButtonLocation.endFloat,
    FloatingActionButtonLocation.endTop,
    FloatingActionButtonLocation.miniCenterDocked,
    FloatingActionButtonLocation.miniCenterFloat,
    FloatingActionButtonLocation.miniCenterTop,
    FloatingActionButtonLocation.miniEndFloat,
    FloatingActionButtonLocation.miniEndTop,
    FloatingActionButtonLocation.miniStartDocked,
    FloatingActionButtonLocation.miniStartFloat,
    FloatingActionButtonLocation.miniStartTop,
    FloatingActionButtonLocation.startDocked,
    FloatingActionButtonLocation.startFloat,
    FloatingActionButtonLocation.startTop
  ];

  try {
    OffsetDetails? fabLocationOffsetDetails = parseOffset(control, propName);
    if (fabLocationOffsetDetails != null) {
      return CustomFloatingActionButtonLocation(
          dx: fabLocationOffsetDetails.x, dy: fabLocationOffsetDetails.y);
    } else {
      return defValue;
    }
  } catch (e) {
    return fabLocations.firstWhere(
        (l) =>
            l.toString().split('.').last.toLowerCase() ==
            control.attrString(propName, "")!.toLowerCase(),
        orElse: () => defValue);
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
  String toString() => 'CustomFloatingActionButtonLocation';
}
