import 'dart:convert';
import 'dart:ui';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';
import '../utils/shadows.dart';
import 'colors.dart';

TextStyle? getTextStyle(BuildContext context, String styleName) {
  var textTheme = Theme.of(context).textTheme;
  switch (styleName.toLowerCase()) {
    case "displaylarge":
      return textTheme.displayLarge;
    case "displaymedium":
      return textTheme.displayMedium;
    case "displaysmall":
      return textTheme.displaySmall;
    case "headlinelarge":
      return textTheme.headlineLarge;
    case "headlinemedium":
      return textTheme.headlineMedium;
    case "headlinesmall":
      return textTheme.headlineSmall;
    case "titlelarge":
      return textTheme.titleLarge;
    case "titlemedium":
      return textTheme.titleMedium;
    case "titlesmall":
      return textTheme.titleSmall;
    case "labellarge":
      return textTheme.labelLarge;
    case "labelmedium":
      return textTheme.labelMedium;
    case "labelsmall":
      return textTheme.labelSmall;
    case "bodylarge":
      return textTheme.bodyLarge;
    case "bodymedium":
      return textTheme.bodyMedium;
    case "bodysmall":
      return textTheme.bodySmall;
  }
  return null;
}

FontWeight? getFontWeight(String weightName) {
  switch (weightName.toLowerCase()) {
    case "normal":
      return FontWeight.normal;
    case "bold":
      return FontWeight.bold;
    case "w100":
      return FontWeight.w100;
    case "w200":
      return FontWeight.w200;
    case "w300":
      return FontWeight.w300;
    case "w400":
      return FontWeight.w400;
    case "w500":
      return FontWeight.w500;
    case "w600":
      return FontWeight.w600;
    case "w700":
      return FontWeight.w700;
    case "w800":
      return FontWeight.w800;
    case "w900":
      return FontWeight.w900;
  }
  return null;
}

TextStyle? parseTextStyle(ThemeData theme, Control control, String propName) {
  dynamic j;
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }
  j = json.decode(v);
  return textStyleFromJson(theme, j);
}

TextStyle textStyleFromJson(ThemeData theme, Map<String, dynamic> json) {
  var fontWeight = json["weight"] ?? "";

  List<FontVariation> variations = [];
  if (fontWeight.startsWith("w")) {
    variations.add(FontVariation('wght', parseDouble(fontWeight.substring(1))));
  }

  var size = json["size"] ?? theme.textTheme.bodyMedium?.fontSize;

  return TextStyle(
      fontSize: parseDouble(size),
      fontWeight: getFontWeight(fontWeight),
      fontStyle:
          (json["italic"] ?? false) ? FontStyle.italic : FontStyle.normal,
      fontFamily: json["font_family"],
      fontVariations: variations,
      color: HexColor.fromString(theme, json["color"] ?? ""),
      backgroundColor: HexColor.fromString(theme, json["bgcolor"] ?? ""),
      shadows: json["shadow"] != null
          ? boxShadowsFromJSON(theme, json["shadow"])
          : null);
}
