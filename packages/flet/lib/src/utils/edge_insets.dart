import 'dart:convert';

import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'material_state.dart';
import 'numbers.dart';

EdgeInsets? parseEdgeInsets(Control control, String propName,
    [EdgeInsets? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return edgeInsetsFromJson(j1, defaultValue);
}

EdgeInsets? edgeInsetsFromJson(dynamic json, [EdgeInsets? defaultValue]) {
  if (json == null) {
    return defaultValue;
  } else if (json is int || json is double) {
    return EdgeInsets.all(parseDouble(json, 0)!);
  }
  return EdgeInsets.fromLTRB(
      parseDouble(json['l'], 0)!,
      parseDouble(json['t'], 0)!,
      parseDouble(json['r'], 0)!,
      parseDouble(json['b'], 0)!);
}

EdgeInsetsDirectional? parseEdgeInsetsDirectional(
    Control control, String propName,
    [EdgeInsetsDirectional? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return edgeInsetsDirectionalFromJson(j1, defaultValue);
}

EdgeInsetsDirectional? edgeInsetsDirectionalFromJson(dynamic json,
    [EdgeInsetsDirectional? defaultValue]) {
  if (json == null) {
    return defaultValue;
  } else if (json is int || json is double) {
    return EdgeInsetsDirectional.all(parseDouble(json, 0)!);
  }
  return EdgeInsetsDirectional.fromSTEB(
      parseDouble(json['l'], 0)!,
      parseDouble(json['t'], 0)!,
      parseDouble(json['r'], 0)!,
      parseDouble(json['b'], 0)!);
}

WidgetStateProperty<EdgeInsets?>? parseWidgetStateEdgeInsets(
    Control control, String propName,
    [EdgeInsets? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  return getWidgetStateProperty<EdgeInsets?>(
      jsonDecode(v), (jv) => edgeInsetsFromJson(jv), defaultValue);
}
