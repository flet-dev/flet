import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../utils/numbers.dart';
import 'colors.dart';

SystemUiOverlayStyle? parseSystemUiOverlayStyle(
    dynamic value, ThemeData? theme, Brightness? brightness,
    [SystemUiOverlayStyle? defaultValue]) {
  if (value == null) return defaultValue;
  Brightness? invertedBrightness = brightness != null
      ? brightness == Brightness.light
          ? Brightness.dark
          : Brightness.light
      : null;

  return SystemUiOverlayStyle(
      statusBarColor: parseColor(value["status_bar_color"], theme),
      systemNavigationBarColor:
          parseColor(value["system_navigation_bar_color"], theme),
      systemNavigationBarDividerColor:
          parseColor(value["system_navigation_bar_divider_color"], theme),
      systemStatusBarContrastEnforced:
          parseBool(value["enforce_system_status_bar_contrast"]),
      systemNavigationBarContrastEnforced:
          parseBool(value["enforce_system_navigation_bar_contrast"]),
      systemNavigationBarIconBrightness: parseBrightness(
          value["system_navigation_bar_icon_brightness"], invertedBrightness),
      statusBarBrightness:
          parseBrightness(value["status_bar_brightness"], brightness),
      statusBarIconBrightness: parseBrightness(
          value["status_bar_icon_brightness"], invertedBrightness));
}

Brightness? parseBrightness(String? value, [Brightness? defaultValue]) {
  if (value == null) return defaultValue;
  return Brightness.values
          .firstWhereOrNull((e) => e.toString() == value.toLowerCase()) ??
      defaultValue;
}
