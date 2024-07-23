import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'numbers.dart';

MainAxisAlignment? parseMainAxisAlignment(String? alignment,
    [MainAxisAlignment? defValue]) {
  if (alignment == null) {
    return defValue;
  }
  return MainAxisAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == alignment.toLowerCase()) ??
      defValue;
}

CrossAxisAlignment? parseCrossAxisAlignment(String? alignment,
    [CrossAxisAlignment? defValue]) {
  if (alignment == null) {
    return defValue;
  }
  return CrossAxisAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == alignment.toLowerCase()) ??
      defValue;
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

Alignment? parseAlignment(Control control, String propName,
    [Alignment? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return alignmentFromJson(j1, defValue);
}

Alignment? alignmentFromJson(Map<String, dynamic>? json,
    [Alignment? defValue]) {
  if (json == null) {
    return defValue;
  }
  return Alignment(parseDouble(json['x'], 0)!, parseDouble(json['y'],0)!);
}
