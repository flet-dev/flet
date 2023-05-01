import 'dart:convert';

import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
import 'material_state.dart';

ThemeData parseTheme(Control control, String propName, Brightness? brightness,
    {ThemeData? parentTheme}) {
  dynamic j;
  var v = control.attrString(propName);
  if (v != null) {
    j = json.decode(v);
  }
  return themeFromJson(j, brightness, parentTheme);
}

ThemeData themeFromJson(Map<String, dynamic>? json, Brightness? brightness,
    ThemeData? parentTheme) {
  ThemeData? theme = parentTheme;

  var primarySwatch = HexColor.fromString(null, json?["primary_swatch"] ?? "");

  var colorSchemeSeed =
      HexColor.fromString(null, json?["color_scheme_seed"] ?? "");

  if (colorSchemeSeed != null) {
    primarySwatch = null;
  }

  if (colorSchemeSeed == null && primarySwatch == null) {
    colorSchemeSeed = Colors.blue;
  }

  // create new theme
  theme ??= ThemeData(
      primarySwatch:
          primarySwatch != null ? primarySwatch as MaterialColor : null,
      colorSchemeSeed: colorSchemeSeed,
      fontFamily: json?["font_family"],
      brightness: brightness,
      useMaterial3: json?["use_material3"] ?? primarySwatch == null);

  var jcs = json?["color_scheme"];
  var jsbt = json?["scrollbar_theme"];

  return theme.copyWith(
      useMaterial3: json?["use_material3"] ?? theme.useMaterial3,
      visualDensity: json?["visual_density"] != null
          ? parseVisualDensity(json?["visual_density"])
          : theme.visualDensity,
      pageTransitionsTheme: json?["page_transitions"] != null
          ? parsePageTransitions(json?["page_transitions"])
          : theme.pageTransitionsTheme,
      colorScheme: jcs != null
          ? theme.colorScheme.copyWith(
              primary: HexColor.fromString(null, jcs["primary"] ?? ""),
              onPrimary: HexColor.fromString(null, jcs["on_primary"] ?? ""),
              primaryContainer:
                  HexColor.fromString(null, jcs["primary_container"] ?? ""),
              onPrimaryContainer:
                  HexColor.fromString(null, jcs["on_primary_container"] ?? ""),
              secondary: HexColor.fromString(null, jcs["secondary"] ?? ""),
              onSecondary: HexColor.fromString(null, jcs["on_secondary"] ?? ""),
              secondaryContainer:
                  HexColor.fromString(null, jcs["secondary_container"] ?? ""),
              onSecondaryContainer: HexColor.fromString(
                  null, jcs["on_secondary_container"] ?? ""),
              tertiary: HexColor.fromString(null, jcs["tertiary"] ?? ""),
              onTertiary: HexColor.fromString(null, jcs["on_tertiary"] ?? ""),
              tertiaryContainer:
                  HexColor.fromString(null, jcs["tertiary_container"] ?? ""),
              onTertiaryContainer:
                  HexColor.fromString(null, jcs["on_tertiary_container"] ?? ""),
              error: HexColor.fromString(null, jcs["error"] ?? ""),
              onError: HexColor.fromString(null, jcs["on_error"] ?? ""),
              errorContainer:
                  HexColor.fromString(null, jcs["error_container"] ?? ""),
              onErrorContainer:
                  HexColor.fromString(null, jcs["on_error_container"] ?? ""),
              background: HexColor.fromString(null, jcs["background"] ?? ""),
              onBackground:
                  HexColor.fromString(null, jcs["on_background"] ?? ""),
              surface: HexColor.fromString(null, jcs["surface"] ?? ""),
              onSurface: HexColor.fromString(null, jcs["on_surface"] ?? ""),
              surfaceVariant:
                  HexColor.fromString(null, jcs["surface_variant"] ?? ""),
              onSurfaceVariant:
                  HexColor.fromString(null, jcs["on_surface_variant"] ?? ""),
              outline: HexColor.fromString(null, jcs["outline"] ?? ""),
              outlineVariant:
                  HexColor.fromString(null, jcs["outline_variant"] ?? ""),
              shadow: HexColor.fromString(null, jcs["shadow"] ?? ""),
              scrim: HexColor.fromString(null, jcs["scrim"] ?? ""),
              inverseSurface:
                  HexColor.fromString(null, jcs["inverse_surface"] ?? ""),
              onInverseSurface:
                  HexColor.fromString(null, jcs["on_inverse_surface"] ?? ""),
              inversePrimary:
                  HexColor.fromString(null, jcs["inverse_primary"] ?? ""),
              surfaceTint: HexColor.fromString(null, jcs["surface_tint"] ?? ""),
            )
          : null,
      scrollbarTheme: jsbt != null
          ? theme.scrollbarTheme.copyWith(
              trackVisibility: getMaterialStateProperty(
                  jsbt["track_visibility"], (jv) => parseBool(jv), null),
              trackColor: getMaterialStateProperty(jsbt["track_color"],
                  (jv) => HexColor.fromString(theme, jv as String), null),
              trackBorderColor: getMaterialStateProperty(
                  jsbt["track_border_color"],
                  (jv) => HexColor.fromString(theme, jv as String),
                  null),
              thumbVisibility: getMaterialStateProperty(
                  jsbt["thumb_visibility"], (jv) => parseBool(jv), null),
              thumbColor: getMaterialStateProperty(jsbt["thumb_color"],
                  (jv) => HexColor.fromString(theme, jv as String), null),
              thickness: getMaterialStateProperty(
                  jsbt["thickness"], (jv) => parseDouble(jv), null),
              radius: jsbt["radius"] != null
                  ? Radius.circular(parseDouble(jsbt["radius"]))
                  : null,
              crossAxisMargin: jsbt["cross_axis_margin"] != null
                  ? parseDouble(jsbt["cross_axis_margin"])
                  : null,
              mainAxisMargin: jsbt["main_axis_margin"] != null
                  ? parseDouble(jsbt["main_axis_margin"])
                  : null,
              minThumbLength: jsbt["min_thumb_length"] != null
                  ? parseDouble(jsbt["min_thumb_length"])
                  : null,
              interactive: jsbt["interactive"] != null
                  ? parseBool(jsbt["interactive"])
                  : null,
            )
          : null);
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
