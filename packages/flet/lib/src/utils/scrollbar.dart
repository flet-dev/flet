import 'package:flutter/material.dart';

import '../models/control.dart';
import 'borders.dart';
import 'enums.dart';
import 'numbers.dart';
import 'platform.dart';

enum ScrollMode { auto, adaptive, always, hidden }

ScrollMode? parseScrollMode(String? value, [ScrollMode? defaultValue]) {
  return parseEnum(ScrollMode.values, value, defaultValue);
}

class ScrollbarConfiguration {
  final bool? thumbVisibility;
  final bool? trackVisibility;
  final double? thickness;
  final Radius? radius;
  final bool? interactive;
  final ScrollbarOrientation? orientation;

  const ScrollbarConfiguration({
    this.thumbVisibility,
    this.trackVisibility,
    this.thickness,
    this.radius,
    this.interactive,
    this.orientation,
  });

  factory ScrollbarConfiguration.fromScrollMode(ScrollMode mode) {
    final defaultThickness = isMobilePlatform() ? 4.0 : null;

    switch (mode) {
      case ScrollMode.auto:
        return ScrollbarConfiguration(thickness: defaultThickness);
      case ScrollMode.adaptive:
        return ScrollbarConfiguration(
            thumbVisibility: !isMobilePlatform(), thickness: defaultThickness);
      case ScrollMode.always:
        return ScrollbarConfiguration(
            thumbVisibility: true, thickness: defaultThickness);
      case ScrollMode.hidden:
        return const ScrollbarConfiguration(thickness: 0);
    }
  }
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
    return mode == null
        ? defaultValue
        : ScrollbarConfiguration.fromScrollMode(mode);
  }

  final baseConfiguration = ScrollbarConfiguration.fromScrollMode(
      parseScrollMode(value["mode"], ScrollMode.auto)!);

  return ScrollbarConfiguration(
    thumbVisibility:
        parseBool(value["thumb_visibility"], baseConfiguration.thumbVisibility),
    trackVisibility:
        parseBool(value["track_visibility"], baseConfiguration.trackVisibility),
    thickness: parseDouble(value["thickness"], baseConfiguration.thickness),
    radius: parseRadius(value["radius"], baseConfiguration.radius),
    interactive: parseBool(value["interactive"], baseConfiguration.interactive),
    orientation: parseScrollbarOrientation(
        value["orientation"], baseConfiguration.orientation),
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
