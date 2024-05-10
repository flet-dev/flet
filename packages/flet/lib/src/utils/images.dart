import 'dart:convert';
import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'gradient.dart';
import 'numbers.dart';

export 'images_io.dart' if (dart.library.js) "images_web.dart";

ImageRepeat parseImageRepeat(Control control, String propName) {
  return ImageRepeat.values.firstWhere(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString(propName, "")!.toLowerCase(),
      orElse: () => ImageRepeat.noRepeat);
}

BoxFit? parseBoxFit(Control control, String propName) {
  return BoxFit.values.firstWhereOrNull((e) =>
      e.name.toLowerCase() == control.attrString(propName, "")!.toLowerCase());
}

ImageFilter? parseBlur(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
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
    tileMode = parseTileMode(json["tile_mode"]);
  }

  return ImageFilter.blur(sigmaX: sigmaX, sigmaY: sigmaY, tileMode: tileMode);
}
