import 'dart:convert';
import 'dart:ui' as ui;

import 'package:collection/collection.dart';
import 'package:flet/src/utils/others.dart';
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

PaintingStyle? parsePaintingStyle(String? value, [PaintingStyle? defValue]) {
  if (value == null) {
    return defValue;
  }
  return PaintingStyle.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

List<double>? parsePaintStrokeDashPattern(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);

  return j1["stroke_dash_pattern"] != null
      ? (j1["stroke_dash_pattern"] as List)
          .map((e) => parseDouble(e))
          .whereNotNull()
          .toList()
      : null;
}

Paint paintFromJSON(ThemeData? theme, Map<String, dynamic> json) {
  var paint = Paint();
  if (json["color"] != null) {
    paint.color = parseColor(theme, json["color"] as String, Colors.black)!;
  }
  paint.blendMode = parseBlendMode(json["blend_mode"], BlendMode.srcOver)!;
  paint.isAntiAlias = parseBool(json["anti_alias"], true)!;
  paint.imageFilter = blurImageFilterFromJSON(json["blur_image"]);
  paint.shader = paintGradientFromJSON(theme, json["gradient"]);
  paint.strokeMiterLimit = parseDouble(json["stroke_miter_limit"], 4)!;
  paint.strokeWidth = parseDouble(json["stroke_width"], 0)!;
  paint.strokeCap = parseStrokeCap(json["stroke_cap"], StrokeCap.butt)!;
  paint.strokeJoin = parseStrokeJoin(json["stroke_join"], StrokeJoin.miter)!;
  paint.style = parsePaintingStyle(json["style"], PaintingStyle.fill)!;
  return paint;
}

ui.Gradient? paintGradientFromJSON(
    ThemeData? theme, Map<String, dynamic>? json) {
  if (json == null) {
    return null;
  }
  String type = json["type"];
  if (type == "linear") {
    return ui.Gradient.linear(
        offsetFromJson(json["begin"])!,
        offsetFromJson(json["end"])!,
        parseColors(theme, json["colors"]),
        parseStops(json["color_stops"]),
        parseTileMode(json["tile_mode"], TileMode.clamp)!);
  } else if (type == "radial") {
    return ui.Gradient.radial(
      offsetFromJson(json["center"])!,
      parseDouble(json["radius"], 0)!,
      parseColors(theme, json["colors"]),
      parseStops(json["color_stops"]),
      parseTileMode(json["tile_mode"], TileMode.clamp)!,
      null,
      offsetFromJson(json["focal"]),
      parseDouble(json["focal_radius"], 0)!,
    );
  } else if (type == "sweep") {
    Offset center = offsetFromJson(json["center"])!;
    return ui.Gradient.sweep(
        center,
        parseColors(theme, json["colors"]),
        parseStops(json["color_stops"]),
        parseTileMode(json["tile_mode"], TileMode.clamp)!,
        parseDouble(json["start_angle"], 0)!,
        parseDouble(json["end_angle"], 0)!,
        parseRotationToMatrix4(
            json["rotation"], Rect.fromCircle(center: center, radius: 10)));
  }
  return null;
}

Offset? offsetFromJson(dynamic json) {
  if (json == null) {
    return null;
  } else if (json is List && json.length > 1) {
    return Offset(parseDouble(json[0], 0)!, parseDouble(json[1], 0)!);
  } else {
    return Offset(parseDouble(json["x"], 0)!, parseDouble(json["y"], 0)!);
  }
}
