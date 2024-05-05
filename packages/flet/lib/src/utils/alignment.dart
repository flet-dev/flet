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

TabAlignment? parseTabAlignment(String? alignment, [TabAlignment? defValue]) {
  if (alignment == null) {
    return defValue;
  }
  return TabAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == alignment.toLowerCase()) ??
      defValue;
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

WrapCrossAlignment? parseWrapCrossAlignment(String? alignment,
    [WrapCrossAlignment? defValue]) {
  if (alignment == null) {
    return defValue;
  }
  return WrapCrossAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == alignment.toLowerCase()) ??
      defValue;
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
