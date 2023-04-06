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

extension GradientExtension on Gradient {
  /// Returns colorStops
  ///
  /// if [stops] provided, returns it directly,
  /// Otherwise we calculate it using colors list
  List<double> getSafeColorStops() {
    var resultStops = <double>[];
    if (stops == null || stops!.length != colors.length) {
      if (colors.length > 1) {
        /// provided colorStops is invalid and we calculate it here
        colors.asMap().forEach((index, color) {
          final percent = 1.0 / (colors.length - 1);
          resultStops.add(percent * index);
        });
      } else {
        throw ArgumentError('"colors" must have length > 1.');
      }
    } else {
      resultStops = stops!;
    }
    return resultStops;
  }
}

/// Lerps between a [LinearGradient] colors, based on [t]
Color lerpGradient(List<Color> colors, List<double> stops, double t) {
  final length = colors.length;
  if (stops.length != length) {
    /// provided gradientColorStops is invalid and we calculate it here
    stops = List.generate(length, (i) => (i + 1) / length);
  }

  for (var s = 0; s < stops.length - 1; s++) {
    final leftStop = stops[s];
    final rightStop = stops[s + 1];

    final leftColor = colors[s];
    final rightColor = colors[s + 1];

    if (t <= leftStop) {
      return leftColor;
    } else if (t < rightStop) {
      final sectionT = (t - leftStop) / (rightStop - leftStop);
      return Color.lerp(leftColor, rightColor, sectionT)!;
    }
  }
  return colors.last;
}
