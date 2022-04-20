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

Border? parseBorder(BuildContext context, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return borderFromJSON(context, j1);
}

BorderRadius borderRadiusFromJSON(Map<String, dynamic> json) {
  return BorderRadius.only(
    topLeft: Radius.circular(parseDouble(json['tl'])),
    topRight: Radius.circular(parseDouble(json['tr'])),
    bottomLeft: Radius.circular(parseDouble(json['bl'])),
    bottomRight: Radius.circular(parseDouble(json['br'])),
  );
}

Border borderFromJSON(BuildContext? context, Map<String, dynamic> json) {
  return Border(
      top: borderSideFromJSON(context, json['t']),
      right: borderSideFromJSON(context, json['r']),
      bottom: borderSideFromJSON(context, json['b']),
      left: borderSideFromJSON(context, json['l']));
}

BorderSide borderSideFromJSON(
    BuildContext? context, Map<String, dynamic> json) {
  return BorderSide(
      color: json['c'] != null
          ? HexColor.fromString(context, json['c'] as String) ?? Colors.black
          : Colors.black,
      width: parseDouble(json['w'], 1),
      style: BorderStyle.solid);
}
