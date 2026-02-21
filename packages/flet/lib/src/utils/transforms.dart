import 'package:flutter/material.dart';

import '../models/control.dart';
import 'alignment.dart';
import 'images.dart';
import 'numbers.dart';

RotationDetails? parseRotationDetails(dynamic value,
    [RotationDetails? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is int || value is double) {
    return RotationDetails(
      angle: parseDouble(value, 0)!,
      alignment: Alignment.center,
      origin: null,
      transformHitTests: true,
      filterQuality: null,
    );
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
      alignment: Alignment.center,
      origin: null,
      transformHitTests: true,
      filterQuality: null,
    );
  }

  return ScaleDetails.fromJson(value);
}

OffsetDetails? parseOffsetDetails(dynamic value,
    [OffsetDetails? defaultValue]) {
  if (value == null) return defaultValue;
  return OffsetDetails.fromValue(value);
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

FlipDetails? parseFlipDetails(dynamic value, [FlipDetails? defaultValue]) {
  if (value == null) return defaultValue;
  return FlipDetails.fromJson(value);
}

TransformDetails? parseTransformDetails(dynamic value,
    [TransformDetails? defaultValue]) {
  if (value == null) return defaultValue;
  return TransformDetails.fromJson(value);
}

class RotationDetails {
  final double angle;
  final Alignment alignment;
  final Offset? origin;
  final bool transformHitTests;
  final FilterQuality? filterQuality;

  RotationDetails({
    required this.angle,
    required this.alignment,
    required this.origin,
    required this.transformHitTests,
    required this.filterQuality,
  });

  factory RotationDetails.fromJson(Map<dynamic, dynamic> value) {
    return RotationDetails(
      angle: parseDouble(value["angle"], 0)!,
      alignment: parseAlignment(value["alignment"], Alignment.center)!,
      origin: parseOffset(value["origin"]),
      transformHitTests: parseBool(value["transform_hit_tests"], true)!,
      filterQuality: parseFilterQuality(value["filter_quality"]),
    );
  }
}

class ScaleDetails {
  final double? scale;
  final double? scaleX;
  final double? scaleY;
  final Alignment alignment;
  final Offset? origin;
  final bool transformHitTests;
  final FilterQuality? filterQuality;

  ScaleDetails({
    required this.scale,
    required this.scaleX,
    required this.scaleY,
    required this.alignment,
    required this.origin,
    required this.transformHitTests,
    required this.filterQuality,
  });

  factory ScaleDetails.fromJson(Map<dynamic, dynamic> value) {
    return ScaleDetails(
      scale: parseDouble(value["scale"]),
      scaleX: parseDouble(value["scale_x"]),
      scaleY: parseDouble(value["scale_y"]),
      alignment: parseAlignment(value["alignment"], Alignment.center)!,
      origin: parseOffset(value["origin"]),
      transformHitTests: parseBool(value["transform_hit_tests"], true)!,
      filterQuality: parseFilterQuality(value["filter_quality"]),
    );
  }
}

class OffsetDetails {
  final double x;
  final double y;
  final bool transformHitTests;
  final FilterQuality? filterQuality;

  OffsetDetails({
    required this.x,
    required this.y,
    required this.transformHitTests,
    required this.filterQuality,
  });

  factory OffsetDetails.fromValue(dynamic value) {
    if (value is List && value.length > 1) {
      return OffsetDetails(
        x: parseDouble(value[0], 0)!,
        y: parseDouble(value[1], 0)!,
        transformHitTests: true,
        filterQuality: null,
      );
    }

    return OffsetDetails(
      x: parseDouble(value["x"], 0)!,
      y: parseDouble(value["y"], 0)!,
      transformHitTests: parseBool(value["transform_hit_tests"], true)!,
      filterQuality: parseFilterQuality(value["filter_quality"]),
    );
  }
}

class FlipDetails {
  final bool flipX;
  final bool flipY;
  final Offset? origin;
  final bool transformHitTests;
  final FilterQuality? filterQuality;

  FlipDetails({
    required this.flipX,
    required this.flipY,
    required this.origin,
    required this.transformHitTests,
    required this.filterQuality,
  });

  factory FlipDetails.fromJson(Map<dynamic, dynamic> value) {
    return FlipDetails(
      flipX: parseBool(value["flip_x"], false)!,
      flipY: parseBool(value["flip_y"], false)!,
      origin: parseOffset(value["origin"]),
      transformHitTests: parseBool(value["transform_hit_tests"], true)!,
      filterQuality: parseFilterQuality(value["filter_quality"]),
    );
  }
}

class TransformDetails {
  final Matrix4 matrix;
  final Offset? origin;
  final Alignment? alignment;
  final bool transformHitTests;
  final FilterQuality? filterQuality;

  TransformDetails({
    required this.matrix,
    required this.origin,
    required this.alignment,
    required this.transformHitTests,
    required this.filterQuality,
  });

  factory TransformDetails.fromJson(Map<dynamic, dynamic> value) {
    return TransformDetails(
      matrix: Matrix4Recording.fromJson(value["matrix"]).replay(),
      origin: parseOffset(value["origin"]),
      alignment: parseAlignment(value["alignment"]),
      transformHitTests: parseBool(value["transform_hit_tests"], true)!,
      filterQuality: parseFilterQuality(value["filter_quality"]),
    );
  }
}

class Matrix4Call {
  final String name;
  final List<dynamic> args;

  Matrix4Call({required this.name, required this.args});

  factory Matrix4Call.fromJson(Map<dynamic, dynamic> value) {
    return Matrix4Call(
      name: value["name"],
      args: value["args"] is List ? List<dynamic>.from(value["args"]) : [],
    );
  }
}

class Matrix4Recording {
  final Matrix4Call ctor;
  final List<Matrix4Call> ops;

  Matrix4Recording({required this.ctor, required this.ops});

  factory Matrix4Recording.fromJson(dynamic value) {
    if (value is! Map) {
      throw ArgumentError("matrix must be a map");
    }

    return Matrix4Recording(
      ctor: Matrix4Call.fromJson(
          value["ctor"] is Map ? value["ctor"] : {"name": "identity"}),
      ops: value["ops"] is List
          ? (value["ops"] as List)
              .whereType<Map>()
              .map((e) => Matrix4Call.fromJson(e))
              .toList()
          : [],
    );
  }

  Matrix4 replay() {
    final matrix = _createMatrix(ctor);
    for (final op in ops) {
      _applyOperation(matrix, op);
    }
    return matrix;
  }

  Matrix4 _createMatrix(Matrix4Call call) {
    switch (call.name) {
      case "identity":
        return Matrix4.identity();
      case "translation_values":
        return Matrix4.translationValues(
          parseDouble(_arg(call.args, 0), 0)!,
          parseDouble(_arg(call.args, 1), 0)!,
          parseDouble(_arg(call.args, 2), 0)!,
        );
      case "diagonal3_values":
        return Matrix4.diagonal3Values(
          parseDouble(_arg(call.args, 0), 1)!,
          parseDouble(_arg(call.args, 1), 1)!,
          parseDouble(_arg(call.args, 2), 1)!,
        );
      case "rotation_z":
        return Matrix4.rotationZ(parseDouble(_arg(call.args, 0), 0)!);
      case "skew_x":
        return Matrix4.skewX(parseDouble(_arg(call.args, 0), 0)!);
      case "skew_y":
        return Matrix4.skewY(parseDouble(_arg(call.args, 0), 0)!);
      default:
        throw UnsupportedError("Unsupported Matrix4 constructor: ${call.name}");
    }
  }

  void _applyOperation(Matrix4 matrix, Matrix4Call call) {
    switch (call.name) {
      case "translate":
        matrix.translateByDouble(
          parseDouble(_arg(call.args, 0), 0)!,
          parseDouble(_arg(call.args, 1), 0)!,
          parseDouble(_arg(call.args, 2), 0)!,
          1.0,
        );
        return;
      case "scale":
        if (call.args.length <= 1) {
          final s = parseDouble(_arg(call.args, 0), 1)!;
          matrix.scaleByDouble(s, s, s, 1.0);
        } else if (call.args.length == 2) {
          matrix.scaleByDouble(
            parseDouble(_arg(call.args, 0), 1)!,
            parseDouble(_arg(call.args, 1), 1)!,
            1.0,
            1.0,
          );
        } else {
          matrix.scaleByDouble(
            parseDouble(_arg(call.args, 0), 1)!,
            parseDouble(_arg(call.args, 1), 1)!,
            parseDouble(_arg(call.args, 2), 1)!,
            1.0,
          );
        }
        return;
      case "rotate_z":
        matrix.rotateZ(parseDouble(_arg(call.args, 0), 0)!);
        return;
      case "rotate_x":
        matrix.rotateX(parseDouble(_arg(call.args, 0), 0)!);
        return;
      case "rotate_y":
        matrix.rotateY(parseDouble(_arg(call.args, 0), 0)!);
        return;
      case "set_entry":
        matrix.setEntry(
          parseInt(_arg(call.args, 0), 0)!,
          parseInt(_arg(call.args, 1), 0)!,
          parseDouble(_arg(call.args, 2), 0)!,
        );
        return;
      case "multiply":
        matrix.multiply(Matrix4Recording.fromJson(_arg(call.args, 0)).replay());
        return;
      default:
        throw UnsupportedError("Unsupported Matrix4 operation: ${call.name}");
    }
  }

  dynamic _arg(List<dynamic> args, int index, [dynamic defaultValue]) {
    return args.length > index ? args[index] : defaultValue;
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

  OffsetDetails? getOffsetDetails(String propertyName,
      [OffsetDetails? defaultValue]) {
    return parseOffsetDetails(get(propertyName), defaultValue);
  }

  Offset? getOffset(String propertyName, [Offset? defaultValue]) {
    return parseOffset(get(propertyName), defaultValue);
  }

  List<Offset>? getOffsetList(String propertyName,
      [List<Offset>? defaultValue]) {
    return parseOffsetList(get(propertyName), defaultValue);
  }

  FlipDetails? getFlipDetails(String propertyName,
      [FlipDetails? defaultValue]) {
    return parseFlipDetails(get(propertyName), defaultValue);
  }

  TransformDetails? getTransformDetails(String propertyName,
      [TransformDetails? defaultValue]) {
    return parseTransformDetails(get(propertyName), defaultValue);
  }
}
