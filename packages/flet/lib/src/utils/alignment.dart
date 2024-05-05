import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'numbers.dart';

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

TabAlignment parseTabAlignment(
    Control control, String propName, TabAlignment defValue) {
  return TabAlignment.values.firstWhere(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString(propName, "")!.toLowerCase(),
      orElse: () => defValue);
}

WrapAlignment? parseWrapAlignment(String? alignment,
    [WrapAlignment? defValue]) {
  if (alignment == null) {
    return defValue;
  }
  return WrapAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == alignment.toLowerCase()) ??
      defValue;
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
  return Alignment(parseDouble(json['x']), parseDouble(json['y']));
}
