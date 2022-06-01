import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
import 'numbers.dart';

BorderRadius? parseBorderRadius(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return borderRadiusFromJSON(j1);
}

Border? parseBorder(ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return borderFromJSON(theme, j1);
}

BorderRadius borderRadiusFromJSON(Map<String, dynamic> json) {
  return BorderRadius.only(
    topLeft: Radius.circular(parseDouble(json['tl'])),
    topRight: Radius.circular(parseDouble(json['tr'])),
    bottomLeft: Radius.circular(parseDouble(json['bl'])),
    bottomRight: Radius.circular(parseDouble(json['br'])),
  );
}

Border borderFromJSON(ThemeData? theme, Map<String, dynamic> json) {
  return Border(
      top: borderSideFromJSON(theme, json['t']),
      right: borderSideFromJSON(theme, json['r']),
      bottom: borderSideFromJSON(theme, json['b']),
      left: borderSideFromJSON(theme, json['l']));
}

BorderSide borderSideFromJSON(ThemeData? theme, Map<String, dynamic> json) {
  return BorderSide(
      color: json['c'] != null
          ? HexColor.fromString(theme, json['c'] as String) ?? Colors.black
          : Colors.black,
      width: parseDouble(json['w'], 1),
      style: BorderStyle.solid);
}
