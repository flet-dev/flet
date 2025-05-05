import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'numbers.dart';

RotationDetails? parseRotationDetails(dynamic value,
    [RotationDetails? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is int || value is double) {
    return RotationDetails(
        angle: parseDouble(value, 0)!, alignment: Alignment.center);
  }

  return RotationDetails.fromJson(value);
}

ScaleDetails? parseScale(dynamic value, [ScaleDetails? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is int || value is double) {
    return ScaleDetails(
        scale: parseDouble(value),
        scaleX: null,
        scaleY: null,
        alignment: Alignment.center);
  }

  return ScaleDetails.fromJson(value);
}

Offset? parseOffset(dynamic value, [Offset? defaultValue]) {
  if (value == null) return defaultValue;
  var details = OffsetDetails.fromValue(value);
  return Offset(details.x, details.y);
}

List<Offset>? parseOffsetList(dynamic value, [List<Offset>? defaultValue]) {
  if (value == null) return defaultValue;
  return (value as List).map((e) => parseOffset(e)).nonNulls.toList();
}

class RotationDetails {
  final double angle;
  final Alignment alignment;

  RotationDetails({required this.angle, required this.alignment});

  factory RotationDetails.fromJson(Map<dynamic, dynamic> value) {
    return RotationDetails(
        angle: parseDouble(value["angle"], 0)!,
        alignment: parseAlignment(value["alignment"], Alignment.center)!);
  }
}

class ScaleDetails {
  final double? scale;
  final double? scaleX;
  final double? scaleY;
  final Alignment alignment;

  ScaleDetails(
      {required this.scale,
      required this.scaleX,
      required this.scaleY,
      required this.alignment});

  factory ScaleDetails.fromJson(Map<dynamic, dynamic> value) {
    return ScaleDetails(
        scale: parseDouble(value["scale"]),
        scaleX: parseDouble(value["scale_x"]),
        scaleY: parseDouble(value["scale_y"]),
        alignment: parseAlignment(value["alignment"], Alignment.center)!);
  }
}

class OffsetDetails {
  final double x;
  final double y;

  OffsetDetails({required this.x, required this.y});

  factory OffsetDetails.fromValue(dynamic value) {
    if (value is List && value.length > 1) {
      return OffsetDetails(
          x: parseDouble(value[0], 0)!, y: parseDouble(value[1], 0)!);
    } else {
      return OffsetDetails(
          x: parseDouble(value["x"], 0)!, y: parseDouble(value["y"], 0)!);
    }
  }
}

extension TransformParsers on Control {
  RotationDetails? getRotationDetails(String propertyName,
      [RotationDetails? defaultValue]) {
    return parseRotationDetails(get(propertyName), defaultValue);
  }

  ScaleDetails? getScale(String propertyName, [ScaleDetails? defaultValue]) {
    return parseScale(get(propertyName), defaultValue);
  }

  Offset? getOffset(String propertyName, [Offset? defaultValue]) {
    return parseOffset(get(propertyName), defaultValue);
  }

  List<Offset>? getOffsetList(String propertyName,
      [List<Offset>? defaultValue]) {
    return parseOffsetList(get(propertyName), defaultValue);
  }
}
