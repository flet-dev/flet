import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

DismissDirection? parseDismissDirection(String? value,
    [DismissDirection? defValue]) {
  if (value == null) {
    return defValue;
  }
  return DismissDirection.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

Map<DismissDirection, double>? parseDismissThresholds(
    Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return getDismissThresholds(j1, (jv) => parseDouble(jv, 0)!);
}

Map<DismissDirection, double>? getDismissThresholds<T>(
    dynamic jsonDictValue, T Function(dynamic) converterFromJson) {
  if (jsonDictValue == null) {
    return null;
  }
  var j = jsonDictValue;
  if (j is! Map<String, dynamic>) {
    j = {"": j};
  }

  return getDismissThresholdsFromJSON(j, converterFromJson);
}

Map<DismissDirection, double> getDismissThresholdsFromJSON(
    Map<String, dynamic>? jsonDictValue, Function(dynamic) converterFromJson) {
  Map<DismissDirection, double> dismissDirectionMap = {};

  if (jsonDictValue != null) {
    jsonDictValue.forEach((directionStr, jv) {
      directionStr
          .split(",")
          .map((s) => s.trim().toLowerCase())
          .forEach((state) {
        DismissDirection d =
            parseDismissDirection(state, DismissDirection.none)!;
        if (d != DismissDirection.none) {
          dismissDirectionMap[d] = converterFromJson(jv);
        }
      });
    });
  }

  return dismissDirectionMap;
}