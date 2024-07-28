import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';
import '../utils/transforms.dart';
import 'colors.dart';

List<BoxShadow> parseBoxShadow(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName);
  if (v == null) {
    return [];
  }

  final j1 = json.decode(v);
  return boxShadowsFromJSON(theme, j1);
}

List<BoxShadow> boxShadowsFromJSON(ThemeData theme, dynamic json) {
  if (json == null) {
    return [];
  }
  if (json is List) {
    return json.map((e) => boxShadowFromJSON(theme, e)).toList();
  } else {
    return [boxShadowFromJSON(theme, json)];
  }
}

BoxShadow boxShadowFromJSON(ThemeData theme, dynamic json) {
  var offset = json["offset"] != null ? offsetFromJSON(json["offset"]) : null;
  return BoxShadow(
      color: parseColor(theme, json["color"], const Color(0xFF000000))!,
      offset: offset != null ? Offset(offset.x, offset.y) : Offset.zero,
      blurStyle: json["blur_style"] != null
          ? BlurStyle.values
              .firstWhere((e) => e.name.toLowerCase() == json["blur_style"])
          : BlurStyle.normal,
      blurRadius: parseDouble(json["blur_radius"], 0)!,
      spreadRadius: parseDouble(json["spread_radius"], 0)!);
}

BoxDecoration? parseBoxDecoration(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return boxDecorationFromJSON(theme, j1);
}

BoxDecoration? boxDecorationFromJSON(ThemeData theme, dynamic json) {
  if (json == null) {
    return null;
  }
  return BoxDecoration(
    color: parseColor(theme, json["color"]),
    border: borderFromJSON(theme, json["border"]),
    shape: parseBoxShape(json["shape"], BoxShape.rectangle)!,
    borderRadius: borderRadiusFromJSON(json["border_radius"]),
    backgroundBlendMode: parseBlendMode(json["blend_mode"]),
    boxShadow: boxShadowsFromJSON(theme, json["box_shadow"]),
    gradient: gradientFromJSON(theme, json["gradient"]),
  );
}
