import 'dart:typed_data';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'colors.dart';
import 'numbers.dart';

Gradient? parseGradient(dynamic value, ThemeData theme) {
  if (value == null) return null;

  String type = value["type"];
  var colors = parseColors(theme, value["colors"]);
  var stops = parseGradientStops(value["stops"]);
  var rotation = parseRotation(value["rotation"]);
  if (type == "linear") {
    return LinearGradient(
        colors: colors,
        stops: stops,
        begin: parseAlignment(value["begin"], Alignment.centerLeft)!,
        end: parseAlignment(value["end"], Alignment.centerRight)!,
        tileMode: parseTileMode(value["tile_mode"], TileMode.clamp)!,
        transform: rotation);
  } else if (type == "radial") {
    return RadialGradient(
        colors: colors,
        stops: stops,
        center: parseAlignment(value["center"], Alignment.center)!,
        radius: parseDouble(value["radius"], 0.5)!,
        focalRadius: parseDouble(value["focal_radius"], 0)!,
        focal: parseAlignment(value["focal"]),
        tileMode: parseTileMode(value["tile_mode"], TileMode.clamp)!,
        transform: rotation);
  } else if (type == "sweep") {
    return SweepGradient(
        colors: colors,
        center: parseAlignment(value["center"], Alignment.center)!,
        startAngle: parseDouble(value["start_angle"], 0)!,
        endAngle: parseDouble(value["end_angle"], 0)!,
        stops: stops,
        tileMode: parseTileMode(value["tile_mode"], TileMode.clamp)!,
        transform: rotation);
  }
  return null;
}

List<Color> parseColors(dynamic value, ThemeData? theme) {
  return (value as List).map((c) => parseColor(c as String, theme)!).toList();
}

List<double>? parseGradientStops(dynamic value, [List<double>? defaultValue]) {
  if (value == null) return defaultValue;
  List? valueAsList = value as List;
  if (valueAsList.isEmpty) return defaultValue;
  return valueAsList.map((v) => parseDouble(v)).nonNulls.toList();
}

TileMode? parseTileMode(String? value, [TileMode? defaultValue]) {
  if (value == null) return defaultValue;
  return TileMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

GradientRotation? parseRotation(dynamic value,
    [GradientRotation? defaultValue]) {
  if (value == null) return defaultValue;
  return GradientRotation(parseDouble(value, 0)!);
}

Float64List? parseRotationToMatrix4(dynamic value, Rect bounds) {
  if (value == null) return null;
  return GradientRotation(parseDouble(value, 0)!).transform(bounds).storage;
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
extension GradientParsers on Control {
  Gradient? getGradient(String propertyName, ThemeData theme) {
    return parseGradient(get(propertyName), theme);
  }

  List<Color> getColors(String propertyName, ThemeData theme) {
    return parseColors(get(propertyName), theme);
  }

  List<double>? getGradientStops(String propertyName,
      [List<double>? defaultValue]) {
    return parseGradientStops(get(propertyName), defaultValue);
  }

  TileMode? getTileMode(String propertyName, [TileMode? defaultValue]) {
    return parseTileMode(get(propertyName), defaultValue);
  }

  GradientRotation? getGradientRotation(String propertyName,
      [GradientRotation? defaultValue]) {
    return parseRotation(get(propertyName), defaultValue);
  }
}