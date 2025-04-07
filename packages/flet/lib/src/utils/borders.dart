import 'dart:collection';

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
  if (value == null) return defaultValue;

  return Radius.circular(value);
}

Border? parseBorder(dynamic value, ThemeData? theme,
    {Color? defaultSideColor,
    BorderSide? defaultBorderSide,
    Border? defaultValue}) {
  if (value == null) return defaultValue;
  return Border(
      top: parseBorderSide(value['top'], theme,
          defaultSideColor: defaultSideColor, defaultValue: defaultBorderSide)!,
      right: parseBorderSide(value['right'], theme,
          defaultSideColor: defaultSideColor, defaultValue: defaultBorderSide)!,
      bottom: parseBorderSide(value['bottom'], theme,
          defaultSideColor: defaultSideColor, defaultValue: defaultBorderSide)!,
      left: parseBorderSide(value['left'], theme,
          defaultSideColor: defaultSideColor,
          defaultValue: defaultBorderSide)!);
}

BorderSide? parseBorderSide(dynamic value, ThemeData? theme,
    {Color? defaultSideColor = Colors.black, BorderSide? defaultValue}) {
  if (value == null) return defaultValue;
  return BorderSide(
      color: parseColor(value['color'], theme, defaultSideColor)!,
      width: parseDouble(value['width'], 1)!,
      strokeAlign:
          parseDouble(value['stroke_align'], BorderSide.strokeAlignInside)!,
      style: BorderStyle.solid);
}

OutlinedBorder? parseOutlinedBorder(dynamic value,
    {BorderRadius? defaultBorderRadius = BorderRadius.zero,
    OutlinedBorder? defaultValue}) {
  if (value == null) return defaultValue;

  String type = value["type"];
  if (type == "roundedRectangle") {
    return RoundedRectangleBorder(
        borderRadius: parseBorderRadius(value["radius"], defaultBorderRadius)!);
  } else if (type == "stadium") {
    return const StadiumBorder();
  } else if (type == "circle") {
    return const CircleBorder();
  } else if (type == "beveledRectangle") {
    return BeveledRectangleBorder(
        borderRadius: parseBorderRadius(value["radius"], defaultBorderRadius)!);
  } else if (type == "continuousRectangle") {
    return ContinuousRectangleBorder(
        borderRadius: parseBorderRadius(value["radius"], defaultBorderRadius)!);
  }
  return defaultValue;
}

OutlinedBorder? parseShape(dynamic value,
    {BorderRadius? defaultBorderRadius = BorderRadius.zero,
    OutlinedBorder? defaultValue}) {
  return parseOutlinedBorder(value,
      defaultBorderRadius: defaultBorderRadius, defaultValue: defaultValue);
}

WidgetStateBorderSide? parseWidgetStateBorderSide(
    dynamic value, ThemeData theme,
    {BorderSide defaultBorderSide = BorderSide.none,
    WidgetStateBorderSide? defaultValue}) {
  if (value == null) return defaultValue;
  if (value is Map<String, dynamic> &&
      (value.containsKey("width") || value.containsKey("color"))) {
    value = {"default": value};
  }

  return WidgetStateBorderSideFromJSON(
      value, (jv) => parseBorderSide(jv, theme), defaultBorderSide);
}

class WidgetStateBorderSideFromJSON extends WidgetStateBorderSide {
  late final Map<String, BorderSide?> _states;
  late final BorderSide _defaultValue;

  WidgetStateBorderSideFromJSON(
      Map<String, dynamic>? jsonDictValue,
      BorderSide? Function(dynamic) converterFromJson,
      BorderSide defaultValue) {
    _defaultValue = defaultValue;

    // preserve user-defined order
    _states = LinkedHashMap<String, BorderSide?>.from(
      jsonDictValue?.map((k, v) {
            var key = k.trim().toLowerCase();
            // "" is deprecated and renamed to "default"
            if (key == "") key = "default";
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
    dynamic value,
    {OutlinedBorder? defaultOutlinedBorder,
    WidgetStateProperty<OutlinedBorder?>? defaultValue}) {
  if (value == null) return defaultValue;

  return getWidgetStateProperty<OutlinedBorder?>(
      value, (jv) => parseOutlinedBorder(jv), defaultOutlinedBorder);
}

extension BorderParsers on Control {
  BorderRadius? getBorderRadius(String propertyName,
      [BorderRadius? defaultValue]) {
    return parseBorderRadius(get(propertyName), defaultValue);
  }

  Radius? getRadius(String propertyName, [Radius? defaultValue]) {
    return parseRadius(get(propertyName), defaultValue);
  }

  Border? getBorder(String propertyName, ThemeData theme,
      {Color? defaultSideColor,
      BorderSide? defaultBorderSide,
      Border? defaultValue}) {
    return parseBorder(get(propertyName), theme,
        defaultSideColor: defaultSideColor,
        defaultBorderSide: defaultBorderSide,
        defaultValue: defaultValue);
  }

  BorderSide? getBorderSide(String propertyName, ThemeData theme,
      {Color? defaultSideColor = Colors.black, BorderSide? defaultValue}) {
    return parseBorderSide(get(propertyName), theme,
        defaultSideColor: defaultSideColor, defaultValue: defaultValue);
  }

  OutlinedBorder? getOutlinedBorder(String propertyName,
      {BorderRadius? defaultBorderRadius = BorderRadius.zero,
      OutlinedBorder? defaultValue}) {
    return parseOutlinedBorder(get(propertyName),
        defaultBorderRadius: defaultBorderRadius, defaultValue: defaultValue);
  }

  OutlinedBorder? getShape(String propertyName,
      {BorderRadius? defaultBorderRadius = BorderRadius.zero,
      OutlinedBorder? defaultValue}) {
    return parseShape(get(propertyName),
        defaultBorderRadius: defaultBorderRadius, defaultValue: defaultValue);
  }

  WidgetStateBorderSide? getWidgetStateBorderSide(
      String propertyName, ThemeData theme,
      {BorderSide defaultBorderSide = BorderSide.none,
      WidgetStateBorderSide? defaultValue}) {
    return parseWidgetStateBorderSide(get(propertyName), theme,
        defaultBorderSide: defaultBorderSide, defaultValue: defaultValue);
  }

  WidgetStateProperty<OutlinedBorder?>? getWidgetStateOutlinedBorder(
      String propertyName,
      {OutlinedBorder? defaultOutlinedBorder,
      WidgetStateProperty<OutlinedBorder?>? defaultValue}) {
    return parseWidgetStateOutlinedBorder(get(propertyName),
        defaultOutlinedBorder: defaultOutlinedBorder,
        defaultValue: defaultValue);
  }
}
