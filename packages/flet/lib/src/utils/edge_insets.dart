import 'package:flutter/widgets.dart';

import 'material_state.dart';
import 'numbers.dart';

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
