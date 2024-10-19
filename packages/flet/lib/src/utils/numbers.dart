import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'material_state.dart';

double? parseDouble(dynamic v, [double? defValue]) {
  if (v is double) {
    return v;
  } else if (v is String && v.toLowerCase() == "inf") {
    return double.infinity;
  } else if (v == null) {
    return defValue;
  } else {
    return double.tryParse(v.toString()) ?? defValue;
  }
}

WidgetStateProperty<double?>? parseWidgetStateDouble(
    Control control, String propName,
    [double? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }
  return getWidgetStateProperty<double?>(
      jsonDecode(v), (jv) => parseDouble(jv), defaultValue);
}

int? parseInt(dynamic v, [int? defValue]) {
  if (v is int) {
    return v;
  } else if (v == null) {
    return defValue;
  } else {
    return int.tryParse(v.toString()) ?? defValue;
  }
}

WidgetStateProperty<int?>? parseWidgetStateInt(Control control, String propName,
    [int? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }
  return getWidgetStateProperty<int?>(
      jsonDecode(v), (jv) => parseInt(jv), defaultValue);
}

bool? parseBool(dynamic v, [bool? defValue]) {
  if (v is bool) {
    return v;
  } else if (v == null) {
    return defValue;
  } else {
    return "true" == v.toString().toLowerCase();
  }
}

WidgetStateProperty<bool?>? parseWidgetStateBool(
    Control control, String propName,
    [bool? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }
  return getWidgetStateProperty<bool?>(
      jsonDecode(v), (jv) => parseBool(jv), defaultValue);
}
