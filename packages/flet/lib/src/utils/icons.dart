import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import 'cupertino_icons.dart';
import 'material_icons.dart';
import 'material_state.dart';

IconData? parseIcon(String? icon, [IconData? defaultIcon]) {
  if (icon == null) {
    return defaultIcon;
  }

  final j1 = json.decode(icon);
  return iconDataFromJson(j1, defaultIcon);
}


IconData? iconDataFromJson(dynamic json, [IconData? defaultIcon]) {
  if (json == null) {
    return defaultIcon;
  } else if (json is String) {
    String icon = json.toLowerCase();
    return materialIcons[icon] ?? cupertinoIcons[icon];
  }
  return IconData(
    json['code_point'] as int,
    fontFamily: json['font_family'] as String?,
    fontPackage: json['font_package'] as String?,
    matchTextDirection: json['match_text_direction'] as bool? ?? false,
    fontFamilyFallback: (json['font_family_fallback'] as List<dynamic>?)
        ?.map((item) => item as String)
        .toList(),
  );
}

WidgetStateProperty<Icon?>? parseWidgetStateIcon(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);

  return getWidgetStateProperty<Icon?>(
      j1, (jv) => Icon(parseIcon(jv as String)));
}
