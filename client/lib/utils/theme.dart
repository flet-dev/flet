import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';

ThemeData? parseTheme(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return themeFromJson(j1);
}

ThemeData themeFromJson(Map<String, dynamic> json) {
  return ThemeData(
      brightness: Brightness.values.firstWhere(
          (b) => b.name.toLowerCase() == json["brightness"],
          orElse: () => Brightness.light),
      colorSchemeSeed:
          HexColor.fromString(null, json["color_scheme_seed"] ?? ""),
      fontFamily: json["font_family"],
      useMaterial3: json["use_material3"]);
}
