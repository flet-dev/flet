import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';

ThemeData parseTheme(Control control, String propName, Brightness? brightness,
    {ThemeData? parentTheme}) {
  dynamic j;
  var v = control.attrString(propName, null);
  if (v != null) {
    j = json.decode(v);
  }
  return themeFromJson(j, brightness, parentTheme);
}

ThemeData themeFromJson(Map<String, dynamic>? json, Brightness? brightness,
    ThemeData? parentTheme) {
  // deal with color scheme
  ColorScheme? colorScheme;

  // try creating scheme from a primary swatch (old method)
  var primaryColorSwatch =
      HexColor.fromString(null, json?["primary_color_swatch"] ?? "");
  if (primaryColorSwatch != null) {
    colorScheme = ColorScheme.fromSwatch(
        primarySwatch: primaryColorSwatch as MaterialColor,
        brightness: brightness ?? Brightness.light);
  }

  // try creating scheme from a seed color
  var colorSchemeSeed =
      HexColor.fromString(null, json?["color_scheme_seed"] ?? "");
  if (colorSchemeSeed != null) {
    colorScheme = ColorScheme.fromSeed(
        seedColor: colorSchemeSeed, brightness: brightness ?? Brightness.light);
  }

  // take original color scheme from parent
  if (parentTheme != null && colorScheme == null) {
    colorScheme = parentTheme.colorScheme;
  }

  // create default scheme
  colorScheme ??= ColorScheme.fromSeed(
      seedColor: Colors.blue, brightness: brightness ?? Brightness.light);

  var jcs = json?["color_scheme"];
  if (jcs != null) {
    colorScheme = colorScheme.copyWith(
        primary: HexColor.fromString(null, jcs["primary"] ?? ""),
        onPrimary: HexColor.fromString(null, jcs["on_primary"] ?? ""),
        primaryContainer:
            HexColor.fromString(null, jcs["primary_container"] ?? ""),
        onPrimaryContainer:
            HexColor.fromString(null, jcs["on_primary_container"] ?? ""));
  }

  var theme = parentTheme ??
      ThemeData(
          colorScheme: colorScheme,
          fontFamily: json?["font_family"],
          brightness: brightness,
          useMaterial3: json?["use_material3"] ?? true,
          visualDensity: parseVisualDensity(json?["visual_density"]),
          pageTransitionsTheme:
              parsePageTransitions(json?["page_transitions"]));
  return theme.copyWith(
      brightness: brightness ?? theme.brightness,
      useMaterial3: json?["use_material3"] ?? theme.useMaterial3,
      visualDensity: json?["visual_density"] != null
          ? parseVisualDensity(json?["visual_density"])
          : theme.visualDensity,
      pageTransitionsTheme: json?["page_transitions"] != null
          ? parsePageTransitions(json?["page_transitions"])
          : theme.pageTransitionsTheme,
      colorScheme: colorScheme);
}

VisualDensity parseVisualDensity(String? vd) {
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
    case "none":
      return const NoPageTransitionsBuilder();
    default:
      return defaultBuilder;
  }
}

class NoPageTransitionsBuilder extends PageTransitionsBuilder {
  const NoPageTransitionsBuilder();

  @override
  Widget buildTransitions<T>(
    PageRoute<T>? route,
    BuildContext? context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget? child,
  ) {
    // only return the child without warping it with animations
    return child!;
  }
}
