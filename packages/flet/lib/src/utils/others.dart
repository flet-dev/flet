import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../models/control.dart';
import 'numbers.dart';

Clip? parseClip(String? value, [Clip? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return Clip.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Orientation? parseOrientation(String? value,
    [Orientation? defaultOrientation]) {
  if (value == null) {
    return defaultOrientation;
  }
  return Orientation.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultOrientation;
}

StrokeCap? parseStrokeCap(String? value, [StrokeCap? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return StrokeCap.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

StrokeJoin? parseStrokeJoin(String? value, [StrokeJoin? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return StrokeJoin.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

BoxShape? parseBoxShape(String? value, [BoxShape? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return BoxShape.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

NotchedShape? parseNotchedShape(String? value, [NotchedShape? defaultValue]) {
  if (value == null) {
    return defaultValue;
  } else if (value == "circular") {
    return const CircularNotchedRectangle();
  } else if (value == "auto") {
    return const AutomaticNotchedShape(ContinuousRectangleBorder());
  } else {
    return defaultValue;
  }
}

SliderInteraction? parseSliderInteraction(String? value,
    [SliderInteraction? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return SliderInteraction.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Size? parseSize(Control control, String propName, [Size? defaultValue]) {
  var v = control.get(propName);
  if (v == null) {
    return defaultValue;
  }
  return sizeFromJson(v, defaultValue);
}

Size? sizeFromJson(Map<String, dynamic>? json, [Size? defaultValue]) {
  if (json == null) return defaultValue;

  final width = parseDouble(json['width']);
  final height = parseDouble(json['height']);

  if (width == null || height == null) return defaultValue;

  return Size(width, height);
}

SnackBarBehavior? parseSnackBarBehavior(String? value,
    [SnackBarBehavior? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return SnackBarBehavior.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

StackFit? parseStackFit(String? value, [StackFit? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return StackFit.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerMode? parseDatePickerMode(String? value,
    [DatePickerMode? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return DatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerEntryMode? parseDatePickerEntryMode(String? value,
    [DatePickerEntryMode? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return DatePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

enum CardVariant { elevated, filled, outlined }

CardVariant? parseCardVariant(String? value, [CardVariant? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return CardVariant.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

enum ScrollMode { none, auto, adaptive, always, hidden }

ScrollMode? parseScrollMode(String? value,
    [ScrollMode? defaultValue = ScrollMode.none]) {
  if (value == null) {
    return defaultValue;
  }
  return ScrollMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

enum LabelPosition { right, left }

LabelPosition? parseLabelPosition(String? value,
    [LabelPosition? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return LabelPosition.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

CupertinoTimerPickerMode? parseCupertinoTimerPickerMode(String? value,
    [CupertinoTimerPickerMode? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return CupertinoTimerPickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ListTileControlAffinity? parseListTileControlAffinity(String? value,
    [ListTileControlAffinity? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return ListTileControlAffinity.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ListTileStyle? parseListTileStyle(String? value,
    [ListTileStyle? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return ListTileStyle.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

NavigationDestinationLabelBehavior? parseNavigationDestinationLabelBehavior(
    String? value,
    [NavigationDestinationLabelBehavior? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return NavigationDestinationLabelBehavior.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

PopupMenuPosition? parsePopupMenuPosition(String? value,
    [PopupMenuPosition? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return PopupMenuPosition.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Assertiveness? parseAssertiveness(String? value,
    [Assertiveness? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return Assertiveness.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerDateOrder? parseDatePickerDateOrder(String? value,
    [DatePickerDateOrder? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return DatePickerDateOrder.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

CupertinoDatePickerMode? parseCupertinoDatePickerMode(String? value,
    [CupertinoDatePickerMode? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return CupertinoDatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ListTileTitleAlignment? parseListTileTitleAlignment(String? value,
    [ListTileTitleAlignment? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return ListTileTitleAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TimePickerEntryMode? parseTimePickerEntryMode(String? value,
    [TimePickerEntryMode? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return TimePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Axis? parseAxis(String? value, [Axis? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return Axis.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

PointerDeviceKind? parsePointerDeviceKind(String? value,
    [PointerDeviceKind? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return PointerDeviceKind.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}
