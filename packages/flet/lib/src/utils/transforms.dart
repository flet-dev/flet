import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'numbers.dart';

RotationDetails? parseRotate(Control control, String propName,
    [RotationDetails? defaultValue]) {
  var v = control.attrString(propName);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return rotateFromJSON(j1, defaultValue);
}

RotationDetails rotateFromJSON(dynamic json, [RotationDetails? defaultValue]) {
  if (json == null) {
    return defaultValue!;
  }
  if (json is int || json is double) {
    return RotationDetails(
        angle: parseDouble(json, 0)!, alignment: Alignment.center);
  }

  return RotationDetails.fromJson(json);
}

ScaleDetails? parseScale(Control control, String propName,
    [ScaleDetails? defaultValue]) {
  var v = control.attrString(propName);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return scaleFromJSON(j1, defaultValue);
}

ScaleDetails? scaleFromJSON(dynamic json, [ScaleDetails? defaultValue]) {
  if (json == null) {
    return defaultValue;
  }
  if (json is int || json is double) {
    return ScaleDetails(
        scale: parseDouble(json),
        scaleX: null,
        scaleY: null,
        alignment: Alignment.center);
  }

  return ScaleDetails.fromJson(json);
}

Offset? parseOffset(Control control, String propName, [Offset? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return offsetFromJSON(j1, defaultValue);
}

Offset? offsetFromJSON(dynamic json, [Offset? defaultValue]) {
  if (json == null) {
    return defaultValue;
  }
  var details = offsetDetailsFromJSON(json);
  return Offset(details.x, details.y);
}

List<Offset>? parseOffsetList(Control control, String propName,
    [List<Offset>? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return (j1 as List).map((e) => offsetFromJSON(e)).whereNotNull().toList();
}

OffsetDetails offsetDetailsFromJSON(dynamic json) {
  return OffsetDetails.fromJson(json);
}

class RotationDetails {
  final double angle;
  final Alignment alignment;

  RotationDetails({required this.angle, required this.alignment});

  factory RotationDetails.fromJson(Map<String, dynamic> json) {
    return RotationDetails(
        angle: parseDouble(json["angle"], 0)!,
        alignment: alignmentFromJson(json["alignment"], Alignment.center)!);
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

  factory ScaleDetails.fromJson(Map<String, dynamic> json) {
    return ScaleDetails(
        scale: parseDouble(json["scale"]),
        scaleX: parseDouble(json["scale_x"]),
        scaleY: parseDouble(json["scale_y"]),
        alignment: alignmentFromJson(json["alignment"], Alignment.center)!);
  }
}

class OffsetDetails {
  final double x;
  final double y;

  OffsetDetails({required this.x, required this.y});

  factory OffsetDetails.fromJson(dynamic json) {
    if (json is List && json.length > 1) {
      return OffsetDetails(
          x: parseDouble(json[0], 0)!, y: parseDouble(json[1], 0)!);
    } else {
      return OffsetDetails(
          x: parseDouble(json["x"], 0)!, y: parseDouble(json["y"], 0)!);
    }
  }
}
