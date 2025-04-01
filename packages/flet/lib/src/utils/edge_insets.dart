import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'material_state.dart';
import 'numbers.dart';

EdgeInsets? parseEdgeInsets(Control control, String propName,
    [EdgeInsets? defaultValue]) {
  var v = control.get(propName);
  if (v == null) {
    return defaultValue;
  }
  return edgeInsetsFromJson(v, defaultValue);
}

EdgeInsets? edgeInsetsFromJson(dynamic json, [EdgeInsets? defaultValue]) {
  if (json == null) {
    return defaultValue;
  } else if (json is int || json is double) {
    return EdgeInsets.all(parseDouble(json, 0)!);
  }
  return EdgeInsets.fromLTRB(
      parseDouble(json['left'], 0)!,
      parseDouble(json['top'], 0)!,
      parseDouble(json['right'], 0)!,
      parseDouble(json['bottom'], 0)!);
}

EdgeInsetsDirectional? parseEdgeInsetsDirectional(
    Control control, String propName,
    [EdgeInsetsDirectional? defaultValue]) {
  var v = control.get(propName);
  if (v == null) {
    return defaultValue;
  }
  return edgeInsetsDirectionalFromJson(v, defaultValue);
}

EdgeInsetsDirectional? edgeInsetsDirectionalFromJson(dynamic json,
    [EdgeInsetsDirectional? defaultValue]) {
  if (json == null) {
    return defaultValue;
  } else if (json is int || json is double) {
    return EdgeInsetsDirectional.all(parseDouble(json, 0)!);
  }
  return EdgeInsetsDirectional.fromSTEB(
      parseDouble(json['left'], 0)!,
      parseDouble(json['top'], 0)!,
      parseDouble(json['right'], 0)!,
      parseDouble(json['bottom'], 0)!);
}

WidgetStateProperty<EdgeInsets?>? parseWidgetStateEdgeInsets(
    Control control, String propName,
    [EdgeInsets? defaultValue]) {
  var v = control.get<String>(propName, null);
  if (v == null) {
    return null;
  }

  return getWidgetStateProperty<EdgeInsets?>(
      v, (jv) => edgeInsetsFromJson(jv), defaultValue);
}
