import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

Clip? parseClip(String? clip, [Clip? defaultValue]) {
  if (clip == null) {
    return defaultValue;
  }
  return Clip.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == clip.toLowerCase()) ??
      defaultValue;
}

Orientation? parseOrientation(String? orientation,
    [Orientation? defaultOrientation]) {
  if (orientation == null) {
    return defaultOrientation;
  }
  return Orientation.values.firstWhereOrNull(
          (a) => a.name.toLowerCase() == orientation.toLowerCase()) ??
      defaultOrientation;
}

StrokeCap? parseStrokeCap(String? value, [StrokeCap? defValue]) {
  if (value == null) {
    return defValue;
  }
  return StrokeCap.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

StrokeJoin? parseStrokeJoin(String? value, [StrokeJoin? defValue]) {
  if (value == null) {
    return defValue;
  }
  return StrokeJoin.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}
