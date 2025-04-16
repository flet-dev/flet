import 'dart:convert';
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

BoxShape? parseBoxShape(String? value, [BoxShape? defValue]) {
  if (value == null) {
    return defValue;
  }
  return BoxShape.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

NotchedShape? parseNotchedShape(String? value, [NotchedShape? defValue]) {
  if (value == null) {
    return defValue;
  } else if (value == "circular") {
    return const CircularNotchedRectangle();
  } else if (value == "auto") {
    return const AutomaticNotchedShape(ContinuousRectangleBorder());
  } else {
    return defValue;
  }
}

SliderInteraction? parseSliderInteraction(String? value,
    [SliderInteraction? defValue]) {
  if (value == null) {
    return defValue;
  }
  return SliderInteraction.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

Size? parseSize(Control control, String propName, [Size? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return sizeFromJson(j1, defValue);
}

Size? sizeFromJson(Map<String, dynamic>? json, [Size? defValue]) {
  if (json == null) return defValue;

  final width = parseDouble(json['width']);
  final height = parseDouble(json['height']);

  if (width == null || height == null) return defValue;

  return Size(width, height);
}

SnackBarBehavior? parseSnackBarBehavior(String? value,
    [SnackBarBehavior? defValue]) {
  if (value == null) {
    return defValue;
  }
  return SnackBarBehavior.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

StackFit? parseStackFit(String? value, [StackFit? defValue]) {
  if (value == null) {
    return defValue;
  }
  return StackFit.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

DatePickerMode? parseDatePickerMode(String? value, [DatePickerMode? defValue]) {
  if (value == null) {
    return defValue;
  }
  return DatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

DatePickerEntryMode? parseDatePickerEntryMode(String? value,
    [DatePickerEntryMode? defValue]) {
  if (value == null) {
    return defValue;
  }
  return DatePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

enum CardVariant { elevated, filled, outlined }

CardVariant? parseCardVariant(String? value, [CardVariant? defValue]) {
  if (value == null) {
    return defValue;
  }
  return CardVariant.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

enum ScrollMode { none, auto, adaptive, always, hidden }

ScrollMode? parseScrollMode(String? value, [ScrollMode? defValue]) {
  if (value == null) {
    return defValue;
  }
  return ScrollMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

enum LabelPosition { right, left }

LabelPosition? parseLabelPosition(String? value, [LabelPosition? defValue]) {
  if (value == null) {
    return defValue;
  }
  return LabelPosition.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

CupertinoTimerPickerMode? parseCupertinoTimerPickerMode(String? value,
    [CupertinoTimerPickerMode? defValue]) {
  if (value == null) {
    return defValue;
  }
  return CupertinoTimerPickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

ListTileControlAffinity? parseListTileControlAffinity(String? value,
    [ListTileControlAffinity? defValue]) {
  if (value == null) {
    return defValue;
  }
  return ListTileControlAffinity.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

ListTileStyle? parseListTileStyle(String? value, [ListTileStyle? defValue]) {
  if (value == null) {
    return defValue;
  }
  return ListTileStyle.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

NavigationDestinationLabelBehavior? parseNavigationDestinationLabelBehavior(
    String? value,
    [NavigationDestinationLabelBehavior? defValue]) {
  if (value == null) {
    return defValue;
  }
  return NavigationDestinationLabelBehavior.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

PopupMenuPosition? parsePopupMenuPosition(String? value,
    [PopupMenuPosition? defValue]) {
  if (value == null) {
    return defValue;
  }
  return PopupMenuPosition.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

Assertiveness? parseAssertiveness(String? value, [Assertiveness? defValue]) {
  if (value == null) {
    return defValue;
  }
  return Assertiveness.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

DatePickerDateOrder? parseDatePickerDateOrder(String? value,
    [DatePickerDateOrder? defValue]) {
  if (value == null) {
    return defValue;
  }
  return DatePickerDateOrder.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

CupertinoDatePickerMode? parseCupertinoDatePickerMode(String? value,
    [CupertinoDatePickerMode? defValue]) {
  if (value == null) {
    return defValue;
  }
  return CupertinoDatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

ListTileTitleAlignment? parseListTileTitleAlignment(String? value,
    [ListTileTitleAlignment? defValue]) {
  if (value == null) {
    return defValue;
  }
  return ListTileTitleAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

TimePickerEntryMode? parseTimePickerEntryMode(String? value,
    [TimePickerEntryMode? defValue]) {
  if (value == null) {
    return defValue;
  }
  return TimePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

Axis? parseAxis(String? value, [Axis? defValue]) {
  if (value == null) {
    return defValue;
  }
  return Axis.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

PointerDeviceKind? parsePointerDeviceKind(String? value,
    [PointerDeviceKind? defValue]) {
  if (value == null) {
    return defValue;
  }
  return PointerDeviceKind.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}
