import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';

Map<DismissDirection, double>? parseDismissThresholds(
    Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return getDismissThresholds(j1, (jv) => parseDouble(jv));
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

  Set<DismissDirection> directions = {
    DismissDirection.vertical,
    DismissDirection.horizontal,
    DismissDirection.endToStart,
    DismissDirection.startToEnd,
    DismissDirection.up,
    DismissDirection.down
  };

  if (jsonDictValue != null) {
    jsonDictValue.forEach((directionStr, jv) {
      directionStr
          .split(",")
          .map((s) => s.trim().toLowerCase())
          .forEach((state) {
        DismissDirection d = directions.firstWhere(
            (e) => e.name.toLowerCase() == state,
            orElse: () => DismissDirection.none);
        if (d != DismissDirection.none) {
          dismissDirectionMap[d] = converterFromJson(jv);
        }
      });
    });
  }

  return dismissDirectionMap;
}
