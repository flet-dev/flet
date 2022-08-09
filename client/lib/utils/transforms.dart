import 'dart:convert';

import 'package:flet_view/utils/alignment.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'numbers.dart';

RotationDetails? parseRotate(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return rotateFromJSON(j1);
}

RotationDetails rotateFromJSON(dynamic json) {
  if (json is int || json is double) {
    return RotationDetails(
        angle: parseDouble(json), alignment: Alignment.center);
  }

  return RotationDetails.fromJson(json);
}

ScaleDetails? parseScale(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return scaleFromJSON(j1);
}

ScaleDetails scaleFromJSON(dynamic json) {
  if (json is int || json is double) {
    return ScaleDetails(
        scale: parseDouble(json),
        scaleX: null,
        scaleY: null,
        alignment: Alignment.center);
  }

  return ScaleDetails.fromJson(json);
}

OffsetDetails? parseOffset(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return OffsetDetails(x: 0, y: 0);
  }

  final j1 = json.decode(v);
  return offsetFromJSON(j1);
}

OffsetDetails offsetFromJSON(dynamic json) {
  return OffsetDetails.fromJson(json);
}

class RotationDetails {
  final double angle;
  final Alignment alignment;

  RotationDetails({required this.angle, required this.alignment});

  factory RotationDetails.fromJson(Map<String, dynamic> json) {
    return RotationDetails(
        angle: parseDouble(json["angle"]),
        alignment: json["alignment"] != null
            ? alignmentFromJson(json["alignment"])
            : Alignment.center);
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
        scale: json["scale"] != null ? parseDouble(json["scale"]) : null,
        scaleX: json["scale_x"] != null ? parseDouble(json["scale_x"]) : null,
        scaleY: json["scale_y"] != null ? parseDouble(json["scale_y"]) : null,
        alignment: json["alignment"] != null
            ? alignmentFromJson(json["alignment"])
            : Alignment.center);
  }
}

class OffsetDetails {
  final double x;
  final double y;

  OffsetDetails({required this.x, required this.y});

  factory OffsetDetails.fromJson(Map<String, dynamic> json) {
    return OffsetDetails(x: parseDouble(json["x"]), y: parseDouble(json["y"]));
  }
}
