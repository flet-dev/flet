import 'dart:convert';
import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import 'colors.dart';
import 'gradient.dart';
import 'numbers.dart';

export 'images_io.dart' if (dart.library.js) "images_web.dart";

ImageRepeat? parseImageRepeat(String? value, [ImageRepeat? defaultValue]) {
  if (value == null) return defaultValue;
  return ImageRepeat.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

BlendMode? parseBlendMode(String? value, [BlendMode? defaultValue]) {
  if (value == null) return defaultValue;
  return BlendMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

BoxFit? parseBoxFit(String? value, [BoxFit? defaultValue]) {
  if (value == null) return defaultValue;
  return BoxFit.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ImageFilter? parseBlur(dynamic value, [ImageFilter? defaultValue]) {
  if (value == null) return defaultValue;

  double sigmaX = 0.0, sigmaY = 0.0;
  TileMode? tileMode;
  if (value is num) {
    sigmaX = sigmaY = parseDouble(value, 0)!;
  } else if (value is List) {
    sigmaX = parseDouble(value.isNotEmpty ? value[0] : 0, 0)!;
    sigmaY = parseDouble(value.length > 1 ? value[1] : value[0], 0)!;
  } else if (value is Map<String, dynamic>) {
    sigmaX = parseDouble(value["sigma_x"], 0)!;
    sigmaY = parseDouble(value["sigma_y"], 0)!;
    tileMode = parseTileMode(value["tile_mode"]);
  }

  return ImageFilter.blur(sigmaX: sigmaX, sigmaY: sigmaY, tileMode: tileMode);
}

ColorFilter? parseColorFilter(dynamic value, ThemeData theme,
    [ColorFilter? defaultValue]) {
  if (value == null) return defaultValue;
  Color? color = parseColor(value["color"], theme);
  BlendMode? blendMode = parseBlendMode(value["blend_mode"]);
  if (color == null || blendMode == null) return defaultValue;
  return ColorFilter.mode(color, blendMode);
}

FilterQuality? parseFilterQuality(String? value,
    [FilterQuality? defaultValue]) {
  if (value == null) return defaultValue;
  return FilterQuality.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

bool isBase64ImageString(String value) {
  // Check for base64 prefix
  final base64PrefixPattern = RegExp(r'^data:image\/[a-zA-Z]+;base64,');
  if (base64PrefixPattern.hasMatch(value)) {
    return true;
  }

  // Check if string contains only valid base64 characters and has a valid length (multiple of 4)
  final base64CharPattern = RegExp(r'^[A-Za-z0-9+/=]+$');
  if (base64CharPattern.hasMatch(value) && value.length % 4 == 0) {
    try {
      base64.decode(value);
      return true;
    } catch (e) {
      return false;
    }
  }

  return false;
}

bool isUrlOrPath(String value) {
  // Check for URL pattern
  final urlPattern = RegExp(r'^(http:\/\/|https:\/\/|www\.)');
  if (urlPattern.hasMatch(value)) {
    return true;
  }

  // Check for common file path characters
  final filePathPattern = RegExp(r'^[a-zA-Z0-9_\-/\\\.]+$');
  if (filePathPattern.hasMatch(value)) {
    return true;
  }

  return false;
}
