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

Border? parseBorder(ThemeData theme, Control control, String propName,
    {Color? defaultSideColor}) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return borderFromJSON(theme, j1, defaultSideColor);
}

BorderRadius borderRadiusFromJSON(dynamic json) {
  if (json is int || json is double) {
    return BorderRadius.all(Radius.circular(parseDouble(json)));
  }
  return BorderRadius.only(
    topLeft: Radius.circular(parseDouble(json['tl'])),
    topRight: Radius.circular(parseDouble(json['tr'])),
    bottomLeft: Radius.circular(parseDouble(json['bl'])),
    bottomRight: Radius.circular(parseDouble(json['br'])),
  );
}

Border borderFromJSON(
    ThemeData? theme, Map<String, dynamic> json, Color? defaultSideColor) {
  return Border(
      top: borderSideFromJSON(theme, json['t'], defaultSideColor),
      right: borderSideFromJSON(theme, json['r'], defaultSideColor),
      bottom: borderSideFromJSON(theme, json['b'], defaultSideColor),
      left: borderSideFromJSON(theme, json['l'], defaultSideColor));
}

BorderSide borderSideFromJSON(
    ThemeData? theme, Map<String, dynamic> json, Color? defaultSideColor) {
  return BorderSide(
      color: json['c'] != null
          ? HexColor.fromString(theme, json['c'] as String) ??
              defaultSideColor ??
              Colors.black
          : Colors.black,
      width: parseDouble(json['w'], 1),
      style: BorderStyle.solid);
}

OutlinedBorder? outlinedBorderFromJSON(Map<String, dynamic> json) {
  String type = json["type"];
  if (type == "roundedRectangle") {
    return RoundedRectangleBorder(
        borderRadius: json["radius"] != null
            ? borderRadiusFromJSON(json["radius"])
            : BorderRadius.zero);
  } else if (type == "stadium") {
    return const StadiumBorder();
  } else if (type == "circle") {
    return const CircleBorder();
  } else if (type == "beveledRectangle") {
    return BeveledRectangleBorder(
        borderRadius: json["radius"] != null
            ? borderRadiusFromJSON(json["radius"])
            : BorderRadius.zero);
  } else if (type == "countinuosRectangle") {
    return ContinuousRectangleBorder(
        borderRadius: json["radius"] != null
            ? borderRadiusFromJSON(json["radius"])
            : BorderRadius.zero);
  }
  return null;
}
