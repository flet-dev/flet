import 'package:flutter/material.dart';

import '../models/control.dart';
import 'enums.dart';
import 'numbers.dart';

enum ScrollMode { none, auto, adaptive, always, hidden }

ScrollMode? parseScrollMode(String? value,
    [ScrollMode? defaultValue = ScrollMode.none]) {
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

  bool get enabled => mode != ScrollMode.none;
}

ScrollbarOrientation? parseScrollbarOrientation(String? value,
    [ScrollbarOrientation? defaultValue]) {
  return parseEnum(ScrollbarOrientation.values, value, defaultValue);
}

ScrollbarConfiguration? parseScrollbarConfiguration(dynamic value,
    [ScrollbarConfiguration? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is! Map) {
    return ScrollbarConfiguration(
      mode: parseScrollMode(value, ScrollMode.none)!,
    );
  }

  final parsedRadius = parseDouble(value["radius"]);
  return ScrollbarConfiguration(
    mode: parseScrollMode(
        value["mode"] ?? value["scroll_mode"], ScrollMode.auto)!,
    thumbVisibility: parseBool(value["thumb_visibility"]),
    trackVisibility: parseBool(value["track_visibility"]),
    thickness: parseDouble(value["thickness"]),
    radius: parsedRadius != null ? Radius.circular(parsedRadius) : null,
    interactive: parseBool(value["interactive"]),
    orientation: parseScrollbarOrientation(value["orientation"]),
  );
}

extension ScrollbarParsers on Control {
  ScrollbarConfiguration? getScrollbarConfiguration(String propertyName,
      [ScrollbarConfiguration? defaultValue]) {
    return parseScrollbarConfiguration(get(propertyName), defaultValue);
  }
}
