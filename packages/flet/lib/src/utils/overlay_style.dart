import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../models/control.dart';
import '../utils/numbers.dart';
import 'colors.dart';

SystemUiOverlayStyle? parseSystemOverlayStyle(
    ThemeData theme, Control control, String propName) {
  dynamic j;
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }
  j = json.decode(v);
  return overlayStyleFromJson(theme, j);
}

SystemUiOverlayStyle overlayStyleFromJson(ThemeData? theme,
    Map<String, dynamic> json) {
  return SystemUiOverlayStyle(
    statusBarColor: json["status_bar_color"] != null
        ? HexColor.fromString(theme, json["status_bar_color"] ?? "")
        : null,
    systemNavigationBarColor: json["system_navigation_bar_color"] != null
        ? HexColor.fromString(theme, json["system_navigation_bar_color"] ?? "")
        : null,
    systemNavigationBarDividerColor:
        json["system_navigation_bar_divider_color"] != null
            ? HexColor.fromString(theme, json["system_navigation_bar_divider_color"] ?? "")
            : null,
    systemStatusBarContrastEnforced:
        json["enforce_system_status_bar_contrast"] != null
            ? parseBool(json["enforce_system_status_bar_contrast"])
            : null,
    systemNavigationBarContrastEnforced:
        json["enforce_system_navigation_bar_contrast"] != null
            ? parseBool(json["enforce_system_navigation_bar_contrast"])
            : null,
  );
}
