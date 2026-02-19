import 'package:flutter/material.dart';

import '../models/control.dart';
import 'numbers.dart';
import 'widget_state.dart';

Size? parseSize(dynamic value, [Size? defaultValue]) {
  if (value == null) return defaultValue;

  final width = parseDouble(value['width']);
  final height = parseDouble(value['height']);

  if (width == null || height == null) return defaultValue;

  return Size(width, height);
}

WidgetStateProperty<Size?>? parseWidgetStateSize(dynamic value,
    {Size? defaultSize, WidgetStateProperty<Size?>? defaultValue}) {
  if (value == null) return defaultValue;

  return getWidgetStateProperty<Size?>(
      value, (jv) => parseSize(jv), defaultSize);
}

Rect? parseRect(dynamic value, [Rect? defaultValue]) {
  if (value == null) return defaultValue;

  final left = parseDouble(value['left']);
  final top = parseDouble(value['top']);
  final right = parseDouble(value['right']);
  final bottom = parseDouble(value['bottom']);

  if (left == null || top == null || right == null || bottom == null) {
    return defaultValue;
  }

  return Rect.fromLTRB(left, top, right, bottom);
}

extension GeometryParsers on Control {
  Size? getSize(String propertyName, [Size? defaultValue]) {
    return parseSize(get(propertyName), defaultValue);
  }

  WidgetStateProperty<Size?>? getWidgetStateSize(String propertyName,
      {Size? defaultSize, WidgetStateProperty<Size?>? defaultValue}) {
    return parseWidgetStateSize(get(propertyName),
        defaultSize: defaultSize, defaultValue: defaultValue);
  }

  Rect? getRect(String propertyName, [Rect? defaultValue]) {
    return parseRect(get(propertyName), defaultValue);
  }
}
