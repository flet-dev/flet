import 'dart:convert';

import 'package:flutter/cupertino.dart';

import '../models/control.dart';

EdgeInsets? parseEdgeInsets(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return edgeInsetsFromJson(j1);
}

EdgeInsets edgeInsetsFromJson(Map<String, dynamic> json) {
  return EdgeInsets.fromLTRB(json['l'] as double, json['t'] as double,
      json['r'] as double, json['b'] as double);
}
