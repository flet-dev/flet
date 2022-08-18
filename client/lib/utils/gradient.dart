import 'dart:convert';

import 'numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'colors.dart';

Gradient? parseGradient(ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return gradientFromJSON(theme, j1);
}

Gradient? gradientFromJSON(ThemeData? theme, Map<String, dynamic> json) {
  String type = json["type"];
  if (type == "linear") {
    return LinearGradient(
        colors: parseColors(theme, json["colors"]),
        stops: parseStops(json["stops"]),
        begin: alignmentFromJson(json["begin"]),
        end: alignmentFromJson(json["end"]),
        tileMode: parseTileMode(json["tile_mode"]),
        transform: parseRotation(json["rotation"]));
  } else if (type == "radial") {
    return RadialGradient(
        colors: parseColors(theme, json["colors"]),
        stops: parseStops(json["stops"]),
        center: alignmentFromJson(json["center"]),
        radius: parseDouble(json["radius"]),
        focalRadius: parseDouble(json["focal_radius"]),
        focal: json["focal"] != null ? alignmentFromJson(json["focal"]) : null,
        tileMode: parseTileMode(json["tile_mode"]),
        transform: parseRotation(json["rotation"]));
  } else if (type == "sweep") {
    return SweepGradient(
        colors: parseColors(theme, json["colors"]),
        center: alignmentFromJson(json["center"]),
        startAngle: parseDouble(json["start_angle"]),
        endAngle: parseDouble(json["end_angle"]),
        stops: parseStops(json["stops"]),
        tileMode: parseTileMode(json["tile_mode"]),
        transform: parseRotation(json["rotation"]));
  }
  return null;
}

List<Color> parseColors(ThemeData? theme, dynamic jv) {
  return (jv as List)
      .map((c) => HexColor.fromString(theme, c as String)!)
      .toList();
}

List<double>? parseStops(dynamic jv) {
  if (jv == null) {
    return null;
  }
  List? list = jv as List;
  if (list.isEmpty) {
    return null;
  }
  return list.map((v) => parseDouble(v)).toList();
}

TileMode parseTileMode(dynamic jv) {
  return jv != null
      ? TileMode.values.firstWhere(
          (e) => e.name.toLowerCase() == jv.toLowerCase(),
          orElse: () => TileMode.clamp)
      : TileMode.clamp;
}

GradientRotation? parseRotation(dynamic jv) {
  if (jv == null) {
    return null;
  }
  return GradientRotation(parseDouble(jv));
}
