import 'dart:convert';

import 'package:flutter/cupertino.dart';

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
    return EdgeInsets.all(parseDouble(json));
  }
  return EdgeInsets.fromLTRB(parseDouble(json['l']), parseDouble(json['t']),
      parseDouble(json['r']), parseDouble(json['b']));
}
