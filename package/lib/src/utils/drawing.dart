import 'dart:convert';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';
import 'colors.dart';
import 'gradient.dart';
import 'images.dart';

Paint parsePaint(ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return Paint();
  }

  final j1 = json.decode(v);

  return paintFromJSON(theme, j1);
}

Paint paintFromJSON(ThemeData? theme, Map<String, dynamic> json) {
  debugPrint("paintFromJSON: $json");
  var paint = Paint();
  if (json["color"] != null) {
    paint.color =
        HexColor.fromString(theme, json["color"] as String) ?? Colors.black;
  }
  if (json["blend_mode"] != null) {
    paint.blendMode = BlendMode.values.firstWhere(
        (e) => e.name.toLowerCase() == json["blend_mode"].toLowerCase(),
        orElse: () => BlendMode.srcOver);
  }
  if (json["anti_alias"] != null) {
    paint.isAntiAlias = json["anti_alias"];
  }
  if (json["blur_image"] != null) {
    paint.imageFilter = blurImageFilterFromJSON(json["blur_image"]);
  }
  if (json["gradient"] != null) {
    paint.shader = gradientFromJSON(theme, json["gradient"]);
  }
  if (json["stroke_miter_limit"] != null) {
    paint.strokeMiterLimit = parseDouble(json["stroke_miter_limit"]);
  }
  if (json["stroke_width"] != null) {
    paint.strokeWidth = parseDouble(json["stroke_width"]);
  }
  if (json["stroke_cap"] != null) {
    paint.strokeCap = StrokeCap.values.firstWhere(
        (e) => e.name.toLowerCase() == json["stroke_cap"].toLowerCase(),
        orElse: () => StrokeCap.butt);
  }
  if (json["stroke_join"] != null) {
    paint.strokeJoin = StrokeJoin.values.firstWhere(
        (e) => e.name.toLowerCase() == json["stroke_join"].toLowerCase(),
        orElse: () => StrokeJoin.miter);
  }
  if (json["style"] != null) {
    paint.style = PaintingStyle.values.firstWhere(
        (e) => e.name.toLowerCase() == json["style"].toLowerCase(),
        orElse: () => PaintingStyle.fill);
  }
  return paint;
}

ui.Gradient? gradientFromJSON(ThemeData? theme, Map<String, dynamic> json) {
  String type = json["type"];
  if (type == "linear") {
    return ui.Gradient.linear(
        offsetFromJson(json["begin"])!,
        offsetFromJson(json["end"])!,
        parseColors(theme, json["colors"]),
        parseStops(json["color_stops"]),
        parseTileMode(json["tile_mode"]));
  } else if (type == "radial") {
    return ui.Gradient.radial(
        offsetFromJson(json["center"])!,
        parseDouble(json["radius"]),
        parseColors(theme, json["colors"]),
        parseStops(json["color_stops"]),
        parseTileMode(json["tile_mode"]),
        null,
        offsetFromJson(json["focal"]),
        parseDouble(json["focal_radius"]));
  } else if (type == "sweep") {
    return ui.Gradient.sweep(
        offsetFromJson(json["center"])!,
        parseColors(theme, json["colors"]),
        parseStops(json["color_stops"]),
        parseTileMode(json["tile_mode"]),
        parseDouble(json["start_angle"]),
        parseDouble(json["end_angle"]));
  }
  return null;
}

Offset? offsetFromJson(dynamic json) {
  if (json == null) {
    return null;
  } else if (json is List && json.length > 1) {
    return Offset(parseDouble(json[0]), parseDouble(json[1]));
  } else {
    return Offset(parseDouble(json["x"]), parseDouble(json["y"]));
  }
}
