import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../models/control.dart';
import 'numbers.dart';

Clip? parseClip(String? value, [Clip? defaultValue]) {
  if (value == null) return defaultValue;
  return Clip.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Orientation? parseOrientation(String? value, [Orientation? defaultValue]) {
  if (value == null) return defaultValue;
  return Orientation.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

StrokeCap? parseStrokeCap(String? value, [StrokeCap? defaultValue]) {
  if (value == null) return defaultValue;
  return StrokeCap.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

StrokeJoin? parseStrokeJoin(String? value, [StrokeJoin? defaultValue]) {
  if (value == null) return defaultValue;
  return StrokeJoin.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

BoxShape? parseBoxShape(String? value, [BoxShape? defaultValue]) {
  if (value == null) return defaultValue;
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
  if (value == null) return defaultValue;
  return SliderInteraction.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Size? parseSize(dynamic value, [Size? defaultValue]) {
  if (value == null) return defaultValue;

  final width = parseDouble(value['width']);
  final height = parseDouble(value['height']);

  if (width == null || height == null) return defaultValue;

  return Size(width, height);
}

SnackBarBehavior? parseSnackBarBehavior(String? value,
    [SnackBarBehavior? defaultValue]) {
  if (value == null) return defaultValue;
  return SnackBarBehavior.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

StackFit? parseStackFit(String? value, [StackFit? defaultValue]) {
  if (value == null) return defaultValue;
  return StackFit.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerMode? parseDatePickerMode(String? value,
    [DatePickerMode? defaultValue]) {
  if (value == null) return defaultValue;
  return DatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerEntryMode? parseDatePickerEntryMode(String? value,
    [DatePickerEntryMode? defaultValue]) {
  if (value == null) return defaultValue;
  return DatePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

enum CardVariant { elevated, filled, outlined }

CardVariant? parseCardVariant(String? value, [CardVariant? defaultValue]) {
  if (value == null) return defaultValue;
  return CardVariant.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

enum ScrollMode { none, auto, adaptive, always, hidden }

ScrollMode? parseScrollMode(String? value,
    [ScrollMode? defaultValue = ScrollMode.none]) {
  if (value == null) return defaultValue;
  return ScrollMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

enum LabelPosition { right, left }

LabelPosition? parseLabelPosition(String? value,
    [LabelPosition? defaultValue]) {
  if (value == null) return defaultValue;
  return LabelPosition.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

CupertinoTimerPickerMode? parseCupertinoTimerPickerMode(String? value,
    [CupertinoTimerPickerMode? defaultValue]) {
  if (value == null) return defaultValue;
  return CupertinoTimerPickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ListTileControlAffinity? parseListTileControlAffinity(String? value,
    [ListTileControlAffinity? defaultValue]) {
  if (value == null) return defaultValue;
  return ListTileControlAffinity.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ListTileStyle? parseListTileStyle(String? value,
    [ListTileStyle? defaultValue]) {
  if (value == null) return defaultValue;
  return ListTileStyle.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

NavigationDestinationLabelBehavior? parseNavigationDestinationLabelBehavior(
    String? value,
    [NavigationDestinationLabelBehavior? defaultValue]) {
  if (value == null) return defaultValue;
  return NavigationDestinationLabelBehavior.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

PopupMenuPosition? parsePopupMenuPosition(String? value,
    [PopupMenuPosition? defaultValue]) {
  if (value == null) return defaultValue;
  return PopupMenuPosition.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Assertiveness? parseAssertiveness(String? value,
    [Assertiveness? defaultValue]) {
  if (value == null) return defaultValue;
  return Assertiveness.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerDateOrder? parseDatePickerDateOrder(String? value,
    [DatePickerDateOrder? defaultValue]) {
  if (value == null) return defaultValue;
  return DatePickerDateOrder.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

CupertinoDatePickerMode? parseCupertinoDatePickerMode(String? value,
    [CupertinoDatePickerMode? defaultValue]) {
  if (value == null) return defaultValue;
  return CupertinoDatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

ListTileTitleAlignment? parseListTileTitleAlignment(String? value,
    [ListTileTitleAlignment? defaultValue]) {
  if (value == null) return defaultValue;
  return ListTileTitleAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TimePickerEntryMode? parseTimePickerEntryMode(String? value,
    [TimePickerEntryMode? defaultValue]) {
  if (value == null) return defaultValue;
  return TimePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

Axis? parseAxis(String? value, [Axis? defaultValue]) {
  if (value == null) return defaultValue;
  return Axis.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

PointerDeviceKind? parsePointerDeviceKind(String? value,
    [PointerDeviceKind? defaultValue]) {
  if (value == null) return defaultValue;
  return PointerDeviceKind.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

NavigationRailLabelType? parseNavigationRailLabelType(String? value,
    [NavigationRailLabelType? defaultValue]) {
  if (value == null) return defaultValue;
  return NavigationRailLabelType.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

extension MiscParsers on Control {
  Clip? getClipBehavior(String propertyName, [Clip? defaultValue]) {
    return parseClip(get(propertyName), defaultValue);
  }

  Orientation? getOrientation(String propertyName,
      [Orientation? defaultValue]) {
    return parseOrientation(get(propertyName), defaultValue);
  }

  StrokeCap? getStrokeCap(String propertyName, [StrokeCap? defaultValue]) {
    return parseStrokeCap(get(propertyName), defaultValue);
  }

  StrokeJoin? getStrokeJoin(String propertyName, [StrokeJoin? defaultValue]) {
    return parseStrokeJoin(get(propertyName), defaultValue);
  }

  BoxShape? getBoxShape(String propertyName, [BoxShape? defaultValue]) {
    return parseBoxShape(get(propertyName), defaultValue);
  }

  NotchedShape? getNotchedShape(String propertyName,
      [NotchedShape? defaultValue]) {
    return parseNotchedShape(get(propertyName), defaultValue);
  }

  SliderInteraction? getSliderInteraction(String propertyName,
      [SliderInteraction? defaultValue]) {
    return parseSliderInteraction(get(propertyName), defaultValue);
  }

  Size? getSize(String propertyName, [Size? defaultValue]) {
    return parseSize(get(propertyName), defaultValue);
  }

  SnackBarBehavior? getSnackBarBehavior(String propertyName,
      [SnackBarBehavior? defaultValue]) {
    return parseSnackBarBehavior(get(propertyName), defaultValue);
  }

  StackFit? getStackFit(String propertyName, [StackFit? defaultValue]) {
    return parseStackFit(get(propertyName), defaultValue);
  }

  DatePickerMode? getDatePickerMode(String propertyName,
      [DatePickerMode? defaultValue]) {
    return parseDatePickerMode(get(propertyName), defaultValue);
  }

  DatePickerEntryMode? getDatePickerEntryMode(String propertyName,
      [DatePickerEntryMode? defaultValue]) {
    return parseDatePickerEntryMode(get(propertyName), defaultValue);
  }

  CardVariant? getCardVariant(String propertyName,
      [CardVariant? defaultValue]) {
    return parseCardVariant(get(propertyName), defaultValue);
  }

  ScrollMode? getScrollMode(String propertyName,
      [ScrollMode? defaultValue = ScrollMode.none]) {
    return parseScrollMode(get(propertyName), defaultValue);
  }

  LabelPosition? getLabelPosition(String propertyName,
      [LabelPosition? defaultValue]) {
    return parseLabelPosition(get(propertyName), defaultValue);
  }

  CupertinoTimerPickerMode? getCupertinoTimerPickerMode(String propertyName,
      [CupertinoTimerPickerMode? defaultValue]) {
    return parseCupertinoTimerPickerMode(get(propertyName), defaultValue);
  }

  ListTileControlAffinity? getListTileControlAffinity(String propertyName,
      [ListTileControlAffinity? defaultValue]) {
    return parseListTileControlAffinity(get(propertyName), defaultValue);
  }

  ListTileStyle? getListTileStyle(String propertyName,
      [ListTileStyle? defaultValue]) {
    return parseListTileStyle(get(propertyName), defaultValue);
  }

  NavigationDestinationLabelBehavior? getNavigationDestinationLabelBehavior(
      String propertyName,
      [NavigationDestinationLabelBehavior? defaultValue]) {
    return parseNavigationDestinationLabelBehavior(
        get(propertyName), defaultValue);
  }

  PopupMenuPosition? getPopupMenuPosition(String propertyName,
      [PopupMenuPosition? defaultValue]) {
    return parsePopupMenuPosition(get(propertyName), defaultValue);
  }

  Assertiveness? getAssertiveness(String propertyName,
      [Assertiveness? defaultValue]) {
    return parseAssertiveness(get(propertyName), defaultValue);
  }

  DatePickerDateOrder? getDatePickerDateOrder(String propertyName,
      [DatePickerDateOrder? defaultValue]) {
    return parseDatePickerDateOrder(get(propertyName), defaultValue);
  }

  CupertinoDatePickerMode? getCupertinoDatePickerMode(String propertyName,
      [CupertinoDatePickerMode? defaultValue]) {
    return parseCupertinoDatePickerMode(get(propertyName), defaultValue);
  }

  ListTileTitleAlignment? getListTileTitleAlignment(String propertyName,
      [ListTileTitleAlignment? defaultValue]) {
    return parseListTileTitleAlignment(get(propertyName), defaultValue);
  }

  TimePickerEntryMode? getTimePickerEntryMode(String propertyName,
      [TimePickerEntryMode? defaultValue]) {
    return parseTimePickerEntryMode(get(propertyName), defaultValue);
  }

  Axis? getAxis(String propertyName, [Axis? defaultValue]) {
    return parseAxis(get(propertyName), defaultValue);
  }

  PointerDeviceKind? getPointerDeviceKind(String propertyName,
      [PointerDeviceKind? defaultValue]) {
    return parsePointerDeviceKind(get(propertyName), defaultValue);
  }

  NavigationRailLabelType? getNavigationRailLabelType(String propertyName,
      [NavigationRailLabelType? defaultValue]) {
    return parseNavigationRailLabelType(get(propertyName), defaultValue);
  }
}