import 'package:flutter/material.dart';

import '../models/control.dart';
import 'borders.dart';
import 'enums.dart';
import 'numbers.dart';

enum ScrollMode { auto, adaptive, always, hidden }

ScrollMode? parseScrollMode(String? value, [ScrollMode? defaultValue]) {
  return parseEnum(ScrollMode.values, value, defaultValue);
}

class ScrollbarConfiguration {
  final ScrollMode mode;
  final bool? thumbVisibility;
  final bool? trackVisibility;
  final double? thickness;
  final Radius? radius;
  final bool? interactive;
  final ScrollbarOrientation? orientation;

  const ScrollbarConfiguration({
    required this.mode,
    this.thumbVisibility,
    this.trackVisibility,
    this.thickness,
    this.radius,
    this.interactive,
    this.orientation,
  });
}

ScrollbarOrientation? parseScrollbarOrientation(String? value,
    [ScrollbarOrientation? defaultValue]) {
  return parseEnum(ScrollbarOrientation.values, value, defaultValue);
}

ScrollbarConfiguration? parseScrollbarConfiguration(dynamic value,
    [ScrollbarConfiguration? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is! Map) {
    final mode = parseScrollMode(value);
    return mode == null ? defaultValue : ScrollbarConfiguration(mode: mode);
  }

  return ScrollbarConfiguration(
    mode: parseScrollMode(
        value["mode"] ?? value["scroll_mode"], ScrollMode.auto)!,
    thumbVisibility: parseBool(value["thumb_visibility"]),
    trackVisibility: parseBool(value["track_visibility"]),
    thickness: parseDouble(value["thickness"]),
    radius: parseRadius(value["radius"]),
    interactive: parseBool(value["interactive"]),
    orientation: parseScrollbarOrientation(value["orientation"]),
  );
}

extension ScrollbarParsers on Control {
  ScrollMode? getScrollMode(String propertyName, [ScrollMode? defaultValue]) {
    return parseScrollMode(get(propertyName), defaultValue);
  }

  ScrollbarConfiguration? getScrollbarConfiguration(String propertyName,
      [ScrollbarConfiguration? defaultValue]) {
    return parseScrollbarConfiguration(get(propertyName), defaultValue);
  }
}
