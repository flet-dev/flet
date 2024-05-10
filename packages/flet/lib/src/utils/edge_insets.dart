import 'dart:convert';

import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'numbers.dart';

EdgeInsets? parseEdgeInsets(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return edgeInsetsFromJson(j1);
}

EdgeInsets edgeInsetsFromJson(dynamic json) {
  if (json is int || json is double) {
    return EdgeInsets.all(parseDouble(json, 0)!);
  }
  return EdgeInsets.fromLTRB(
      parseDouble(json['l'], 0)!,
      parseDouble(json['t'], 0)!,
      parseDouble(json['r'], 0)!,
      parseDouble(json['b'], 0)!);
}

EdgeInsetsDirectional? parseEdgeInsetsDirectional(
    Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return edgeInsetsDirectionalFromJson(j1);
}

EdgeInsetsDirectional edgeInsetsDirectionalFromJson(dynamic json) {
  if (json is int || json is double) {
    return EdgeInsetsDirectional.all(parseDouble(json, 0)!);
  }
  return EdgeInsetsDirectional.fromSTEB(
      parseDouble(json['l'], 0)!,
      parseDouble(json['t'], 0)!,
      parseDouble(json['r'], 0)!,
      parseDouble(json['b'], 0)!);
}
