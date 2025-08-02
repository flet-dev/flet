import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../models/control.dart';
import 'borders.dart';
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

NotchedShape? parseNotchedShape(dynamic value, ThemeData? theme,
    [NotchedShape? defaultValue]) {
  if (value == null) return defaultValue;

  var type = value["_type"];
  if (type == "circular") {
    return CircularNotchedRectangle(
        inverted: parseBool(value["inverted"], false)!);
  } else if (type == "auto") {
    return AutomaticNotchedShape(
        parseShapeBorder(
            value["host"], theme, const ContinuousRectangleBorder())!,
        parseShapeBorder(value["guest"], theme));
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

ListTileTitleAlignment? parseListTileTitleAlignment(String? value,
    [ListTileTitleAlignment? defaultValue]) {
  if (value == null) return defaultValue;
  return ListTileTitleAlignment.values.firstWhereOrNull(
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

BlurStyle? parseBlurStyle(String? value, [BlurStyle? defaultValue]) {
  if (value == null) return defaultValue;
  return BlurStyle.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

FloatingLabelBehavior? parseFloatingLabelBehavior(String? value,
    [FloatingLabelBehavior? defaultValue]) {
  if (value == null) return defaultValue;
  return FloatingLabelBehavior.values.firstWhereOrNull(
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

  NotchedShape? getNotchedShape(String propertyName, ThemeData? theme,
      [NotchedShape? defaultValue]) {
    return parseNotchedShape(get(propertyName), theme, defaultValue);
  }

  SliderInteraction? getSliderInteraction(String propertyName,
      [SliderInteraction? defaultValue]) {
    return parseSliderInteraction(get(propertyName), defaultValue);
  }

  SnackBarBehavior? getSnackBarBehavior(String propertyName,
      [SnackBarBehavior? defaultValue]) {
    return parseSnackBarBehavior(get(propertyName), defaultValue);
  }

  StackFit? getStackFit(String propertyName, [StackFit? defaultValue]) {
    return parseStackFit(get(propertyName), defaultValue);
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

  ListTileTitleAlignment? getListTileTitleAlignment(String propertyName,
      [ListTileTitleAlignment? defaultValue]) {
    return parseListTileTitleAlignment(get(propertyName), defaultValue);
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

  BlurStyle? getBlurStyle(String propertyName, [BlurStyle? defaultValue]) {
    return parseBlurStyle(get(propertyName), defaultValue);
  }

  FloatingLabelBehavior? getFloatingLabelBehavior(String propertyName,
      [FloatingLabelBehavior? defaultValue]) {
    return parseFloatingLabelBehavior(get(propertyName), defaultValue);
  }
}
