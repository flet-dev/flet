import 'dart:collection';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
import 'material_state.dart';
import 'numbers.dart';

BorderRadius? parseBorderRadius(dynamic value, [BorderRadius? defaultValue]) {
  if (value == null) return defaultValue;

  if (value is int || value is double) {
    return BorderRadius.all(parseRadius(value)!);
  }
  return BorderRadius.only(
    topLeft: parseRadius(value['top_left'], Radius.zero)!,
    topRight: parseRadius(value['top_right'], Radius.zero)!,
    bottomLeft: parseRadius(value['bottom_left'], Radius.zero)!,
    bottomRight: parseRadius(value['bottom_right'], Radius.zero)!,
  );
}

Radius? parseRadius(dynamic value, [Radius? defaultValue]) {
  var radius = parseDouble(value);
  if (radius == null) return defaultValue;

  return Radius.circular(radius);
}

BorderStyle? parseBorderStyle(String? value, [BorderStyle? defaultValue]) {
  if (value == null) return defaultValue;
  return BorderStyle.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Border? parseBorder(dynamic value, ThemeData? theme,
    {Color defaultSideColor = Colors.black,
    BorderSide? defaultBorderSide,
    Border? defaultValue}) {
  if (value == null) return defaultValue;
  return Border(
      top: parseBorderSide(value['top'], theme,
          defaultSideColor: defaultSideColor,
          defaultValue: defaultBorderSide ?? BorderSide.none)!,
      right: parseBorderSide(value['right'], theme,
          defaultSideColor: defaultSideColor,
          defaultValue: defaultBorderSide ?? BorderSide.none)!,
      bottom: parseBorderSide(value['bottom'], theme,
          defaultSideColor: defaultSideColor,
          defaultValue: defaultBorderSide ?? BorderSide.none)!,
      left: parseBorderSide(value['left'], theme,
          defaultSideColor: defaultSideColor,
          defaultValue: defaultBorderSide ?? BorderSide.none)!);
}

BorderSide? parseBorderSide(dynamic value, ThemeData? theme,
    {Color defaultSideColor = Colors.black, BorderSide? defaultValue}) {
  if (value == null) return defaultValue;
  return BorderSide(
    color: parseColor(value['color'], theme, defaultSideColor)!,
    width: parseDouble(value['width'], 1)!,
    strokeAlign:
        parseDouble(value['stroke_align'], BorderSide.strokeAlignInside)!,
    style: parseBorderStyle(value['style'], BorderStyle.solid)!,
  );
}

ShapeBorder? parseShapeBorder(dynamic value, ThemeData? theme,
    [ShapeBorder? defaultValue]) {
  if (value == null) return defaultValue;
  return parseOutlinedBorder(value, theme,
      defaultValue: defaultValue as OutlinedBorder?);
}

OutlinedBorder? parseOutlinedBorder(dynamic value, ThemeData? theme,
    {BorderSide defaultBorderSide = BorderSide.none,
    BorderRadius defaultBorderRadius = BorderRadius.zero,
    OutlinedBorder? defaultValue}) {
  if (value == null) return defaultValue;

  var borderSide =
      parseBorderSide(value["side"], theme, defaultValue: defaultBorderSide)!;
  var borderRadius = parseBorderRadius(value["radius"], defaultBorderRadius)!;

  var type = value["_type"];
  switch (type.toLowerCase()) {
    case "roundedrectangle":
      return RoundedRectangleBorder(
          side: borderSide, borderRadius: borderRadius);
    case "stadium":
      return StadiumBorder(side: borderSide);
    case "circle":
      return CircleBorder(
          side: borderSide,
          eccentricity: parseDouble(value["eccentricity"], 0.0)!);
    case "beveledrectangle":
      return BeveledRectangleBorder(
          side: borderSide, borderRadius: borderRadius);
    case "continuousrectangle":
      return ContinuousRectangleBorder(
          side: borderSide, borderRadius: borderRadius);
    default:
      return defaultValue;
  }
}

OutlinedBorder? parseShape(dynamic value, ThemeData? theme,
    {BorderSide defaultBorderSide = BorderSide.none,
    BorderRadius defaultBorderRadius = BorderRadius.zero,
    OutlinedBorder? defaultValue}) {
  return parseOutlinedBorder(value, theme,
      defaultBorderSide: defaultBorderSide,
      defaultBorderRadius: defaultBorderRadius,
      defaultValue: defaultValue);
}

WidgetStateBorderSide? parseWidgetStateBorderSide(
    dynamic value, ThemeData theme,
    {BorderSide? defaultBorderSide = BorderSide.none,
    WidgetStateBorderSide? defaultValue}) {
  if (value == null) return defaultValue;
  if (value is Map &&
      (value.containsKey("width") || value.containsKey("color"))) {
    value = {"default": value};
  }

  return WidgetStateBorderSideFromJSON(
      value, (jv) => parseBorderSide(jv, theme), defaultBorderSide);
}

class WidgetStateBorderSideFromJSON extends WidgetStateBorderSide {
  late final Map<dynamic, BorderSide?> _states;
  late final BorderSide? _defaultValue;

  WidgetStateBorderSideFromJSON(
      Map<dynamic, dynamic>? jsonDictValue,
      BorderSide? Function(dynamic) converterFromJson,
      BorderSide? defaultValue) {
    _defaultValue = defaultValue;

    // preserve user-defined order
    _states = LinkedHashMap<String, BorderSide?>.from(
      jsonDictValue?.map((k, v) {
            var key = k.trim().toLowerCase();
            return MapEntry(key, converterFromJson(v));
          }) ??
          {},
    );
  }

  @override
  BorderSide? resolve(Set<WidgetState> states) {
    // Resolve using user-defined order in _states
    for (var stateName in _states.keys) {
      if (stateName == "default") continue; // Skip "default"; handled last
      if (states.any((state) => state.name == stateName)) {
        return _states[stateName];
      }
    }

    // Default state
    return _states["default"] ?? _defaultValue;
  }
}

WidgetStateProperty<OutlinedBorder?>? parseWidgetStateOutlinedBorder(
    dynamic value, ThemeData? theme,
    {OutlinedBorder? defaultOutlinedBorder,
    WidgetStateProperty<OutlinedBorder?>? defaultValue}) {
  if (value == null) return defaultValue;

  return getWidgetStateProperty<OutlinedBorder?>(
      value, (jv) => parseOutlinedBorder(jv, theme), defaultOutlinedBorder);
}

extension BorderParsers on Control {
  BorderRadius? getBorderRadius(String propertyName,
      [BorderRadius? defaultValue]) {
    return parseBorderRadius(get(propertyName), defaultValue);
  }

  Radius? getRadius(String propertyName, [Radius? defaultValue]) {
    return parseRadius(get(propertyName), defaultValue);
  }

  BorderStyle? getBorderStyle(String propertyName,
      [BorderStyle? defaultValue]) {
    return parseBorderStyle(get(propertyName), defaultValue);
  }

  Border? getBorder(String propertyName, ThemeData theme,
      {Color defaultSideColor = Colors.black,
      BorderSide? defaultBorderSide,
      Border? defaultValue}) {
    return parseBorder(get(propertyName), theme,
        defaultSideColor: defaultSideColor,
        defaultBorderSide: defaultBorderSide,
        defaultValue: defaultValue);
  }

  BorderSide? getBorderSide(String propertyName, ThemeData theme,
      {Color defaultSideColor = Colors.black, BorderSide? defaultValue}) {
    return parseBorderSide(get(propertyName), theme,
        defaultSideColor: defaultSideColor, defaultValue: defaultValue);
  }

  OutlinedBorder? getOutlinedBorder(String propertyName, ThemeData? theme,
      {BorderSide defaultBorderSide = BorderSide.none,
      BorderRadius defaultBorderRadius = BorderRadius.zero,
      OutlinedBorder? defaultValue}) {
    return parseOutlinedBorder(get(propertyName), theme,
        defaultBorderSide: defaultBorderSide,
        defaultBorderRadius: defaultBorderRadius,
        defaultValue: defaultValue);
  }

  OutlinedBorder? getShape(String propertyName, ThemeData? theme,
      {BorderSide defaultBorderSide = BorderSide.none,
      BorderRadius defaultBorderRadius = BorderRadius.zero,
      OutlinedBorder? defaultValue}) {
    return parseOutlinedBorder(get(propertyName), theme,
        defaultBorderSide: defaultBorderSide,
        defaultBorderRadius: defaultBorderRadius,
        defaultValue: defaultValue);
  }

  WidgetStateBorderSide? getWidgetStateBorderSide(
      String propertyName, ThemeData theme,
      {BorderSide defaultBorderSide = BorderSide.none,
      WidgetStateBorderSide? defaultValue}) {
    return parseWidgetStateBorderSide(get(propertyName), theme,
        defaultBorderSide: defaultBorderSide, defaultValue: defaultValue);
  }

  WidgetStateProperty<OutlinedBorder?>? getWidgetStateOutlinedBorder(
      String propertyName, ThemeData? theme,
      {OutlinedBorder? defaultOutlinedBorder,
      WidgetStateProperty<OutlinedBorder?>? defaultValue}) {
    return parseWidgetStateOutlinedBorder(get(propertyName), theme,
        defaultOutlinedBorder: defaultOutlinedBorder,
        defaultValue: defaultValue);
  }
}
