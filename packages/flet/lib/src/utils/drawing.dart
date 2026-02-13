import 'dart:ui' as ui;
import 'enums.dart';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/numbers.dart';
import '../utils/transforms.dart';
import 'colors.dart';
import 'gradient.dart';
import 'images.dart';
import 'misc.dart';

Paint? parsePaint(dynamic value, ThemeData theme, [Paint? defaultValue]) {
  if (value == null) return defaultValue;

  var paint = Paint();
  paint.color = parseColor(value["color"] as String?, theme, Colors.black)!;
  paint.blendMode = parseBlendMode(value["blend_mode"], BlendMode.srcOver)!;
  paint.isAntiAlias = parseBool(value["anti_alias"], true)!;
  paint.imageFilter = parseBlur(value["blur_image"]);
  paint.shader = parsePaintGradient(value["gradient"], theme);
  paint.strokeMiterLimit = parseDouble(value["stroke_miter_limit"], 4)!;
  paint.strokeWidth = parseDouble(value["stroke_width"], 0)!;
  paint.strokeCap = parseStrokeCap(value["stroke_cap"], StrokeCap.butt)!;
  paint.strokeJoin = parseStrokeJoin(value["stroke_join"], StrokeJoin.miter)!;
  paint.style = parsePaintingStyle(value["style"], PaintingStyle.fill)!;
  return paint;
}

PaintingStyle? parsePaintingStyle(String? value,
    [PaintingStyle? defaultValue]) {
  return parseEnum(PaintingStyle.values, value, defaultValue);
}

List<double>? parsePaintStrokeDashPattern(dynamic value,
    [List<double>? defaultValue]) {
  if (value == null) return defaultValue;

  return (value["stroke_dash_pattern"] as List?)
          ?.map((e) => parseDouble(e))
          .nonNulls
          .toList() ??
      defaultValue;
}

ui.Gradient? parsePaintGradient(Map<dynamic, dynamic>? value, ThemeData? theme,
    [ui.Gradient? defaultValue]) {
  if (value == null) return defaultValue;

  var type = value["_type"];
  var colorStops = parseGradientStops(value["color_stops"]);
  var colors = parseColors(value["colors"], theme);
  var tileMode = parseTileMode(value["tile_mode"], TileMode.clamp)!;
  if (type == "linear") {
    return ui.Gradient.linear(parseOffset(value["begin"])!,
        parseOffset(value["end"])!, colors, colorStops, tileMode);
  } else if (type == "radial") {
    return ui.Gradient.radial(
      parseOffset(value["center"])!,
      parseDouble(value["radius"], 0)!,
      colors,
      colorStops,
      tileMode,
      null,
      parseOffset(value["focal"]),
      parseDouble(value["focal_radius"], 0)!,
    );
  } else if (type == "sweep") {
    Offset center = parseOffset(value["center"])!;
    return ui.Gradient.sweep(
        center,
        colors,
        colorStops,
        tileMode,
        parseDouble(value["start_angle"], 0)!,
        parseDouble(value["end_angle"], 0)!,
        parseRotationToMatrix4(
            value["rotation"], Rect.fromCircle(center: center, radius: 10)));
  }
  return defaultValue;
}

extension DrawingParsers on Control {
  Paint? getPaint(String propertyName, ThemeData theme, [Paint? defaultValue]) {
    return parsePaint(get(propertyName), theme, defaultValue);
  }

  PaintingStyle? getPaintingStyle(String propertyName,
      [PaintingStyle? defaultValue]) {
    return parsePaintingStyle(get(propertyName), defaultValue);
  }

  List<double>? getPaintStrokeDashPattern(String propertyName,
      [List<double>? defaultValue]) {
    return parsePaintStrokeDashPattern(get(propertyName), defaultValue);
  }
}
