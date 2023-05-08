import 'dart:convert';

import 'package:flet/src/utils/borders.dart';
import 'package:flet/src/utils/edge_insets.dart';
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

  return theme.copyWith(
      useMaterial3: json?["use_material3"] ?? theme.useMaterial3,
      visualDensity: json?["visual_density"] != null
          ? parseVisualDensity(json?["visual_density"])
          : theme.visualDensity,
      pageTransitionsTheme: json?["page_transitions"] != null
          ? parsePageTransitions(json?["page_transitions"])
          : theme.pageTransitionsTheme,
      colorScheme: parseColorScheme(theme, json?["color_scheme"]),
      scrollbarTheme: parseScrollBarTheme(theme, json?["scrollbar_theme"]),
      tabBarTheme: parseTabBarTheme(theme, json?["tab_bar_theme"]));
}

ColorScheme? parseColorScheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  return theme.colorScheme.copyWith(
    primary: HexColor.fromString(null, j["primary"] ?? ""),
    onPrimary: HexColor.fromString(null, j["on_primary"] ?? ""),
    primaryContainer: HexColor.fromString(null, j["primary_container"] ?? ""),
    onPrimaryContainer:
        HexColor.fromString(null, j["on_primary_container"] ?? ""),
    secondary: HexColor.fromString(null, j["secondary"] ?? ""),
    onSecondary: HexColor.fromString(null, j["on_secondary"] ?? ""),
    secondaryContainer:
        HexColor.fromString(null, j["secondary_container"] ?? ""),
    onSecondaryContainer:
        HexColor.fromString(null, j["on_secondary_container"] ?? ""),
    tertiary: HexColor.fromString(null, j["tertiary"] ?? ""),
    onTertiary: HexColor.fromString(null, j["on_tertiary"] ?? ""),
    tertiaryContainer: HexColor.fromString(null, j["tertiary_container"] ?? ""),
    onTertiaryContainer:
        HexColor.fromString(null, j["on_tertiary_container"] ?? ""),
    error: HexColor.fromString(null, j["error"] ?? ""),
    onError: HexColor.fromString(null, j["on_error"] ?? ""),
    errorContainer: HexColor.fromString(null, j["error_container"] ?? ""),
    onErrorContainer: HexColor.fromString(null, j["on_error_container"] ?? ""),
    background: HexColor.fromString(null, j["background"] ?? ""),
    onBackground: HexColor.fromString(null, j["on_background"] ?? ""),
    surface: HexColor.fromString(null, j["surface"] ?? ""),
    onSurface: HexColor.fromString(null, j["on_surface"] ?? ""),
    surfaceVariant: HexColor.fromString(null, j["surface_variant"] ?? ""),
    onSurfaceVariant: HexColor.fromString(null, j["on_surface_variant"] ?? ""),
    outline: HexColor.fromString(null, j["outline"] ?? ""),
    outlineVariant: HexColor.fromString(null, j["outline_variant"] ?? ""),
    shadow: HexColor.fromString(null, j["shadow"] ?? ""),
    scrim: HexColor.fromString(null, j["scrim"] ?? ""),
    inverseSurface: HexColor.fromString(null, j["inverse_surface"] ?? ""),
    onInverseSurface: HexColor.fromString(null, j["on_inverse_surface"] ?? ""),
    inversePrimary: HexColor.fromString(null, j["inverse_primary"] ?? ""),
    surfaceTint: HexColor.fromString(null, j["surface_tint"] ?? ""),
  );
}

ScrollbarThemeData? parseScrollBarTheme(
    ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }
  return theme.scrollbarTheme.copyWith(
    trackVisibility: getMaterialStateProperty(
        j["track_visibility"], (jv) => parseBool(jv), null),
    trackColor: getMaterialStateProperty(j["track_color"],
        (jv) => HexColor.fromString(theme, jv as String), null),
    trackBorderColor: getMaterialStateProperty(j["track_border_color"],
        (jv) => HexColor.fromString(theme, jv as String), null),
    thumbVisibility: getMaterialStateProperty(
        j["thumb_visibility"], (jv) => parseBool(jv), null),
    thumbColor: getMaterialStateProperty(j["thumb_color"],
        (jv) => HexColor.fromString(theme, jv as String), null),
    thickness:
        getMaterialStateProperty(j["thickness"], (jv) => parseDouble(jv), null),
    radius:
        j["radius"] != null ? Radius.circular(parseDouble(j["radius"])) : null,
    crossAxisMargin: j["cross_axis_margin"] != null
        ? parseDouble(j["cross_axis_margin"])
        : null,
    mainAxisMargin: j["main_axis_margin"] != null
        ? parseDouble(j["main_axis_margin"])
        : null,
    minThumbLength: j["min_thumb_length"] != null
        ? parseDouble(j["min_thumb_length"])
        : null,
    interactive: j["interactive"] != null ? parseBool(j["interactive"]) : null,
  );
}

TabBarTheme? parseTabBarTheme(ThemeData theme, Map<String, dynamic>? j) {
  if (j == null) {
    return null;
  }

  var indicatorColor = HexColor.fromString(theme, j["indicator_color"] ?? "");

  return theme.tabBarTheme.copyWith(
    overlayColor: getMaterialStateProperty(j["overlay_color"],
        (jv) => HexColor.fromString(theme, jv as String), null),
    dividerColor: HexColor.fromString(theme, j["divider_color"] ?? ""),
    indicatorColor: indicatorColor,
    labelColor: HexColor.fromString(theme, j["label_color"] ?? ""),
    unselectedLabelColor:
        HexColor.fromString(theme, j["unselected_label_color"] ?? ""),
    indicatorSize: parseBool(j["indicator_tab_size"], false)
        ? TabBarIndicatorSize.tab
        : TabBarIndicatorSize.label,
    indicator: j["indicator_border_radius"] != null ||
            j["indicator_border_side"] != null ||
            j["indicator_padding"] != null
        ? UnderlineTabIndicator(
            borderRadius: j["indicator_border_radius"] != null
                ? borderRadiusFromJSON(j["indicator_border_radius"])
                : const BorderRadius.only(
                    topLeft: Radius.circular(2), topRight: Radius.circular(2)),
            borderSide: borderSideFromJSON(
                    theme, j["indicator_border_side"], indicatorColor) ??
                BorderSide(
                    width: 2.0,
                    color: indicatorColor ?? theme.colorScheme.primary),
            insets: j["indicator_padding"] != null
                ? edgeInsetsFromJson(j["indicator_padding"])
                : EdgeInsets.zero)
        : null,
  );
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
