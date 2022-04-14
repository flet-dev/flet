import 'package:flet_view/utils/colors.dart';
import 'package:flutter/material.dart';

ThemeData themeFromJson(Map<String, dynamic> json) {
  return ThemeData(
      brightness: Brightness.values.firstWhere(
          (b) => b.name.toLowerCase() == json["brightness"],
          orElse: () => Brightness.light),
      colorSchemeSeed: HexColor.fromString(json["color_scheme_seed"]),
      useMaterial3: json["use_material3"]);
}
