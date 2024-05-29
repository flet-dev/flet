import 'dart:convert';
import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
import 'gradient.dart';
import 'numbers.dart';

export 'images_io.dart' if (dart.library.js) "images_web.dart";

ImageRepeat? parseImageRepeat(String? repeat, [ImageRepeat? defValue]) {
  if (repeat == null) {
    return defValue;
  }
  return ImageRepeat.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == repeat.toLowerCase()) ??
      defValue;
}

BoxFit? parseBoxFit(String? fit, [BoxFit? defValue]) {
  if (fit == null) {
    return defValue;
  }
  return BoxFit.values
          .firstWhereOrNull((e) => e.name.toLowerCase() == fit.toLowerCase()) ??
      defValue;
}

ImageFilter? parseBlur(Control control, String propName,
    [ImageFilter? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return blurImageFilterFromJSON(j1);
}

ImageFilter blurImageFilterFromJSON(dynamic json) {
  double sigmaX = 0.0;
  double sigmaY = 0.0;
  TileMode tileMode = TileMode.clamp;
  if (json is int || json is double) {
    sigmaX = sigmaY = parseDouble(json, 0)!;
  } else if (json is List && json.length > 1) {
    sigmaX = parseDouble(json[0], 0)!;
    sigmaY = parseDouble(json[1], 0)!;
  } else {
    sigmaX = parseDouble(json["sigma_x"], 0)!;
    sigmaY = parseDouble(json["sigma_y"], 0)!;
    tileMode = parseTileMode(json["tile_mode"], TileMode.clamp)!;
  }

  return ImageFilter.blur(sigmaX: sigmaX, sigmaY: sigmaY, tileMode: tileMode);
}

ColorFilter? parseColorFilter(Control control, String propName, ThemeData theme,
    [ColorFilter? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return colorFilterFromJSON(j1, theme);
}

ColorFilter? colorFilterFromJSON(dynamic json, ThemeData theme,
    [ColorFilter? defValue]) {
  Color? color = parseColor(theme, json["color"]);
  BlendMode? blendMode = parseBlendMode(json["blend_mode"]);
  if (color == null || blendMode == null) {
    return defValue;
  }
  return ColorFilter.mode(color, blendMode);
}

FilterQuality? parseFilterQuality(String? quality, [FilterQuality? defValue]) {
  if (quality == null) {
    return defValue;
  }
  return FilterQuality.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == quality.toLowerCase()) ??
      defValue;
}
