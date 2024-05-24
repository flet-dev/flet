import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../utils/numbers.dart';
import 'colors.dart';

SystemUiOverlayStyle overlayStyleFromJson(
    ThemeData? theme, Map<String, dynamic> json, Brightness? brightness) {
  Brightness? invertedBrightness = brightness != null
      ? brightness == Brightness.light
          ? Brightness.dark
          : Brightness.light
      : null;

  return SystemUiOverlayStyle(
      statusBarColor: parseColor(theme, json["status_bar_color"]),
      systemNavigationBarColor:
          parseColor(theme, json["system_navigation_bar_color"]),
      systemNavigationBarDividerColor:
          parseColor(theme, json["system_navigation_bar_divider_color"]),
      systemStatusBarContrastEnforced:
          parseBool(json["enforce_system_status_bar_contrast"]),
      systemNavigationBarContrastEnforced:
          parseBool(json["enforce_system_navigation_bar_contrast"]),
      systemNavigationBarIconBrightness: parseBrightness(
          json["system_navigation_bar_icon_brightness"], invertedBrightness),
      statusBarBrightness:
          parseBrightness(json["status_bar_brightness"], brightness),
      statusBarIconBrightness: parseBrightness(
          json["status_bar_icon_brightness"], invertedBrightness));
}

Brightness? parseBrightness(String? value, [Brightness? defValue]) {
  if (value == null) {
    return defValue;
  }
  return Brightness.values
          .firstWhereOrNull((e) => e.toString() == value.toLowerCase()) ??
      defValue;
}
