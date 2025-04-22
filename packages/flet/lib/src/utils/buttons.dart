import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import '../utils/time.dart';
import '../utils/transforms.dart';
import 'alignment.dart';
import 'borders.dart';
import 'colors.dart';
import 'edge_insets.dart';
import 'material_state.dart';
import 'mouse.dart';
import 'numbers.dart';

ButtonStyle? parseButtonStyle(dynamic value, ThemeData theme,
    {Color? defaultForegroundColor,
    Color? defaultBackgroundColor,
    Color? defaultOverlayColor,
    Color? defaultShadowColor,
    Color? defaultSurfaceTintColor,
    double? defaultElevation,
    EdgeInsets? defaultPadding,
    BorderSide? defaultBorderSide,
    OutlinedBorder? defaultShape,
    ButtonStyle? defaultValue}) {
  if (value == null) return defaultValue;
  return ButtonStyle(
    foregroundColor: parseWidgetStateColor(value["color"], theme,
        defaultColor: defaultForegroundColor),
    backgroundColor: parseWidgetStateColor(value["bgcolor"], theme,
        defaultColor: defaultBackgroundColor),
    overlayColor: parseWidgetStateColor(value["overlay_color"], theme,
        defaultColor: defaultOverlayColor),
    shadowColor: parseWidgetStateColor(value["shadow_color"], theme,
        defaultColor: defaultShadowColor),
    surfaceTintColor: parseWidgetStateColor(value["surface_tint_color"], theme,
        defaultColor: defaultSurfaceTintColor),
    elevation: parseWidgetStateDouble(value["elevation"],
        defaultDouble: defaultElevation),
    animationDuration: parseDuration(value["animation_duration"]),
    padding: getWidgetStateProperty<EdgeInsetsGeometry?>(
        value["padding"], (jv) => parseEdgeInsets(jv), defaultPadding),
    side: getWidgetStateProperty<BorderSide?>(
        value["side"],
        (jv) => parseBorderSide(jv, theme,
            defaultSideColor: theme.colorScheme.outline),
        defaultBorderSide),
    shape: getWidgetStateProperty<OutlinedBorder?>(
        value["shape"], (jv) => parseOutlinedBorder(jv), defaultShape),
    iconColor: parseWidgetStateColor(value["icon_color"], theme,
        defaultColor: defaultForegroundColor),
    alignment: parseAlignment(value["alignment"]),
    enableFeedback: parseBool(value["enable_feedback"]),
    textStyle: getWidgetStateProperty<TextStyle?>(
        value["text_style"], (jv) => parseTextStyle(jv, theme)),
    iconSize: parseWidgetStateDouble(value["icon_size"]),
    visualDensity: parseVisualDensity(value["visual_density"]),
    mouseCursor: parseWidgetStateMouseCursor(value["mouse_cursor"]),
  );
}

FloatingActionButtonLocation? parseFloatingActionButtonLocation(dynamic value,
    [FloatingActionButtonLocation? defaultValue]) {
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
    var fabLocationOffset = parseOffset(value);

    return fabLocationOffset != null
        ? CustomFloatingActionButtonLocation(
            dx: fabLocationOffset.dx, dy: fabLocationOffset.dy)
        : defaultValue;
  } catch (e) {
    var key = value.toLowerCase();
    return fabLocations.containsKey(key) ? fabLocations[key]! : defaultValue;
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

CupertinoButtonSize? parseCupertinoButtonSize(String? value,
    [CupertinoButtonSize? defaultValue]) {
  if (value == null) return defaultValue;
  return CupertinoButtonSize.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

extension ButtonParsers on Control {
  ButtonStyle? getButtonStyle(String propertyName, ThemeData theme,
      {Color? defaultForegroundColor,
      Color? defaultBackgroundColor,
      Color? defaultOverlayColor,
      Color? defaultShadowColor,
      Color? defaultSurfaceTintColor,
      double? defaultElevation,
      EdgeInsets? defaultPadding,
      BorderSide? defaultBorderSide,
      OutlinedBorder? defaultShape,
      ButtonStyle? defaultValue}) {
    return parseButtonStyle(get(propertyName), theme,
        defaultForegroundColor: defaultForegroundColor,
        defaultBackgroundColor: defaultBackgroundColor,
        defaultOverlayColor: defaultOverlayColor,
        defaultShadowColor: defaultShadowColor,
        defaultSurfaceTintColor: defaultSurfaceTintColor,
        defaultElevation: defaultElevation,
        defaultPadding: defaultPadding,
        defaultBorderSide: defaultBorderSide,
        defaultShape: defaultShape,
        defaultValue: defaultValue);
  }

  FloatingActionButtonLocation? getFloatingActionButtonLocation(
      String propertyName,
      [FloatingActionButtonLocation? defaultValue]) {
    return parseFloatingActionButtonLocation(get(propertyName), defaultValue);
  }

  CupertinoButtonSize? getCupertinoButtonSize(String propertyName,
      [CupertinoButtonSize? defaultValue]) {
    return parseCupertinoButtonSize(get(propertyName), defaultValue);
  }
}
