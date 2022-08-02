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
      useMaterial3: json["use_material3"],
      visualDensity: parseVisualDensity(json["visual_density"]));
}

VisualDensity? parseVisualDensity(String? vd) {
  if (vd == null) {
    return null;
  }

  switch (vd.toLowerCase()) {
    case "adaptiveplatformdensity":
      return VisualDensity.adaptivePlatformDensity;
    case "comfortable":
      return VisualDensity.comfortable;
    case "compact":
      return VisualDensity.compact;
    case "standard":
      return VisualDensity.standard;
    default:
      return null;
  }
}
