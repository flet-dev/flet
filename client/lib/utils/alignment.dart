import 'dart:convert';

import 'package:flutter/cupertino.dart';

import '../models/control.dart';

MainAxisAlignment parseMainAxisAlignment(
    Control control, String propName, MainAxisAlignment defValue) {
  return MainAxisAlignment.values.firstWhere(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString(propName, "")!.toLowerCase(),
      orElse: () => defValue);
}

CrossAxisAlignment parseCrossAxisAlignment(
    Control control, String propName, CrossAxisAlignment defValue) {
  return CrossAxisAlignment.values.firstWhere(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString(propName, "")!.toLowerCase(),
      orElse: () => defValue);
}

WrapAlignment parseWrapAlignment(
    Control control, String propName, WrapAlignment defValue) {
  return WrapAlignment.values.firstWhere(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString(propName, "")!.toLowerCase(),
      orElse: () => defValue);
}

WrapCrossAlignment parseWrapCrossAlignment(
    Control control, String propName, WrapCrossAlignment defValue) {
  return WrapCrossAlignment.values.firstWhere(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString(propName, "")!.toLowerCase(),
      orElse: () => defValue);
}

Alignment? parseAlignment(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return alignmentFromJson(j1);
}

Alignment alignmentFromJson(Map<String, dynamic> json) {
  return Alignment(json['x'] as double, json['y'] as double);
}
