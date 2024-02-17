import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../utils/numbers.dart';
import 'colors.dart';

SystemUiOverlayStyle overlayStyleFromJson(
    ThemeData? theme, Map<String, dynamic> json, Brightness? brightness) {
  return SystemUiOverlayStyle(
      statusBarColor: json["status_bar_color"] != null
          ? HexColor.fromString(theme, json["status_bar_color"] ?? "")
          : null,
      systemNavigationBarColor: json["system_navigation_bar_color"] != null
          ? HexColor.fromString(
              theme, json["system_navigation_bar_color"] ?? "")
          : null,
      systemNavigationBarDividerColor:
          json["system_navigation_bar_divider_color"] != null
              ? HexColor.fromString(
                  theme, json["system_navigation_bar_divider_color"] ?? "")
              : null,
      systemStatusBarContrastEnforced:
          json["enforce_system_status_bar_contrast"] != null
              ? parseBool(json["enforce_system_status_bar_contrast"])
              : null,
      systemNavigationBarContrastEnforced:
          json["enforce_system_navigation_bar_contrast"] != null
              ? parseBool(json["enforce_system_navigation_bar_contrast"])
              : null,
      systemNavigationBarIconBrightness: parseBrightness(
          json["system_navigation_bar_icon_brightness"], brightness),
      statusBarBrightness:
          parseBrightness(json["status_bar_brightness"], brightness),
      statusBarIconBrightness:
          parseBrightness(json["status_bar_icon_brightness"], brightness));
}

Brightness? parseBrightness(dynamic value, Brightness? brightness) {
  if (value == null) {
    return null;
  }
  var b = parseBool(value);
  Brightness? invertedBrightness = brightness != null
      ? brightness == Brightness.light
          ? Brightness.dark
          : Brightness.light
      : null;
  return b ? brightness : invertedBrightness;
}
