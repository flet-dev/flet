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

BlendMode? parseBlendMode(String? mode, [BlendMode? defValue]) {
  if (mode == null) {
    return defValue;
  }
  return BlendMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == mode.toLowerCase()) ??
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

ImageFilter? blurImageFilterFromJSON(dynamic json) {
  double sigmaX = 0.0;
  double sigmaY = 0.0;
  TileMode tileMode = TileMode.clamp;
  if (json == null) {
    return null;
  } else if (json is int || json is double) {
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
  if (json == null) {
    return defValue;
  }
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

bool isBase64ImageString(String s) {
  // Check for base64 prefix
  final base64PrefixPattern = RegExp(r'^data:image\/[a-zA-Z]+;base64,');
  if (base64PrefixPattern.hasMatch(s)) {
    return true;
  }

  // Check if string contains only valid base64 characters and has a valid length (multiple of 4)
  final base64CharPattern = RegExp(r'^[A-Za-z0-9+/=]+$');
  if (base64CharPattern.hasMatch(s) && s.length % 4 == 0) {
    try {
      base64.decode(s);
      return true;
    } catch (e) {
      return false;
    }
  }

  return false;
}

bool isUrlOrPath(String s) {
  // Check for URL pattern
  final urlPattern = RegExp(r'^(http:\/\/|https:\/\/|www\.)');
  if (urlPattern.hasMatch(s)) {
    return true;
  }

  // Check for common file path characters
  final filePathPattern = RegExp(r'^[a-zA-Z0-9_\-/\\\.]+$');
  if (filePathPattern.hasMatch(s)) {
    return true;
  }

  return false;
}
