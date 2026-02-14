import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'numbers.dart';
import 'widget_state.dart';

EdgeInsets? parseEdgeInsets(dynamic value, [EdgeInsets? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is int || value is double) {
    return EdgeInsets.all(parseDouble(value, 0)!);
  }
  return EdgeInsets.fromLTRB(
      parseDouble(value['left'], 0)!,
      parseDouble(value['top'], 0)!,
      parseDouble(value['right'], 0)!,
      parseDouble(value['bottom'], 0)!);
}

EdgeInsets? parseMargin(dynamic value, [EdgeInsets? defaultValue]) {
  return parseEdgeInsets(value, defaultValue);
}

EdgeInsets? parsePadding(dynamic value, [EdgeInsets? defaultValue]) {
  return parseEdgeInsets(value, defaultValue);
}

EdgeInsetsDirectional? parseEdgeInsetsDirectional(dynamic value,
    [EdgeInsetsDirectional? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is int || value is double) {
    return EdgeInsetsDirectional.all(parseDouble(value, 0)!);
  }
  return EdgeInsetsDirectional.fromSTEB(
      parseDouble(value['left'], 0)!,
      parseDouble(value['top'], 0)!,
      parseDouble(value['right'], 0)!,
      parseDouble(value['bottom'], 0)!);
}

WidgetStateProperty<EdgeInsets?>? parseWidgetStateEdgeInsets(dynamic value,
    {EdgeInsets? defaultEdgeInsets,
    WidgetStateProperty<EdgeInsets?>? defaultValue}) {
  if (value == null) return defaultValue;

  return getWidgetStateProperty<EdgeInsets?>(
      value, (jv) => parseEdgeInsets(jv), defaultEdgeInsets);
}

WidgetStateProperty<EdgeInsets?>? parseWidgetStatePadding(dynamic value,
    {EdgeInsets? defaultPadding,
    WidgetStateProperty<EdgeInsets?>? defaultValue}) {
  return parseWidgetStateEdgeInsets(value,
      defaultEdgeInsets: defaultPadding, defaultValue: defaultValue);
}

WidgetStateProperty<EdgeInsets?>? parseWidgetStateMargin(dynamic value,
    {EdgeInsets? defaultEdgeInsets,
    WidgetStateProperty<EdgeInsets?>? defaultValue}) {
  return parseWidgetStateEdgeInsets(value,
      defaultEdgeInsets: defaultEdgeInsets, defaultValue: defaultValue);
}

extension EdgeInsetsParsers on Control {
  EdgeInsets? getEdgeInsets(String propertyName, [EdgeInsets? defaultValue]) {
    return parseEdgeInsets(get(propertyName), defaultValue);
  }

  EdgeInsets? getMargin(String propertyName, [EdgeInsets? defaultValue]) {
    return parseMargin(get(propertyName), defaultValue);
  }

  EdgeInsets? getPadding(String propertyName, [EdgeInsets? defaultValue]) {
    return parsePadding(get(propertyName), defaultValue);
  }

  EdgeInsetsDirectional? getEdgeInsetsDirectional(String propertyName,
      [EdgeInsetsDirectional? defaultValue]) {
    return parseEdgeInsetsDirectional(get(propertyName), defaultValue);
  }

  WidgetStateProperty<EdgeInsets?>? getWidgetStateEdgeInsets(
      String propertyName,
      {EdgeInsets? defaultEdgeInsets,
      WidgetStateProperty<EdgeInsets?>? defaultValue}) {
    return parseWidgetStateEdgeInsets(get(propertyName),
        defaultEdgeInsets: defaultEdgeInsets, defaultValue: defaultValue);
  }

  WidgetStateProperty<EdgeInsets?>? getWidgetStatePadding(String propertyName,
      {EdgeInsets? defaultPadding,
      WidgetStateProperty<EdgeInsets?>? defaultValue}) {
    return parseWidgetStatePadding(get(propertyName),
        defaultPadding: defaultPadding, defaultValue: defaultValue);
  }

  WidgetStateProperty<EdgeInsets?>? getWidgetStateMargin(String propertyName,
      {EdgeInsets? defaultEdgeInsets,
      WidgetStateProperty<EdgeInsets?>? defaultValue}) {
    return parseWidgetStateMargin(get(propertyName),
        defaultEdgeInsets: defaultEdgeInsets, defaultValue: defaultValue);
  }
}
