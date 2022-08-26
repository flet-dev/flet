import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';

ThemeData parseTheme(Control control, String propName, Brightness brightness) {
  dynamic j;
  var v = control.attrString(propName, null);
  if (v != null) {
    j = json.decode(v);
  }
  return themeFromJson(j, brightness);
}

ThemeData themeFromJson(Map<String, dynamic>? json, Brightness brightness) {
  return ThemeData(
      brightness: brightness,
      colorSchemeSeed:
          HexColor.fromString(null, json?["color_scheme_seed"] ?? "") ??
              Colors.blue,
      fontFamily: json?["font_family"],
      useMaterial3: json?["use_material3"] ?? true,
      visualDensity: parseVisualDensity(json?["visual_density"]),
      pageTransitionsTheme: parsePageTransitions(json?["page_transitions"]));
}

VisualDensity? parseVisualDensity(String? vd) {
  switch (vd?.toLowerCase()) {
    case "adaptiveplatformdensity":
      return VisualDensity.adaptivePlatformDensity;
    case "comfortable":
      return VisualDensity.comfortable;
    case "compact":
      return VisualDensity.compact;
    default:
      return VisualDensity.standard;
  }
}

PageTransitionsTheme parsePageTransitions(Map<String, dynamic>? json) {
  return PageTransitionsTheme(builders: {
    TargetPlatform.android: parseTransitionsBuilder(
        json?["android"], const FadeUpwardsPageTransitionsBuilder()),
    TargetPlatform.iOS: parseTransitionsBuilder(
        json?["ios"], const CupertinoPageTransitionsBuilder()),
    TargetPlatform.linux: parseTransitionsBuilder(
        json?["linux"], const ZoomPageTransitionsBuilder()),
    TargetPlatform.macOS: parseTransitionsBuilder(
        json?["macos"], const ZoomPageTransitionsBuilder()),
    TargetPlatform.windows: parseTransitionsBuilder(
        json?["windows"], const ZoomPageTransitionsBuilder()),
  });
}

PageTransitionsBuilder parseTransitionsBuilder(
    String? tb, PageTransitionsBuilder defaultBuilder) {
  switch (tb?.toLowerCase()) {
    case "fadeupwards":
      return const FadeUpwardsPageTransitionsBuilder();
    case "openupwards":
      return const OpenUpwardsPageTransitionsBuilder();
    case "cupertino":
      return const CupertinoPageTransitionsBuilder();
    case "zoom":
      return const ZoomPageTransitionsBuilder();
    default:
      return defaultBuilder;
  }
}
