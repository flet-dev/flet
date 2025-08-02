import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'borders.dart';
import 'edge_insets.dart';

TabBarIndicatorSize? parseTabBarIndicatorSize(String? value,
    [TabBarIndicatorSize? defaultValue]) {
  if (value == null) return defaultValue;
  return TabBarIndicatorSize.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

TabIndicatorAnimation? parseTabIndicatorAnimation(String? value,
    [TabIndicatorAnimation? defaultValue]) {
  if (value == null) return defaultValue;
  return TabIndicatorAnimation.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

UnderlineTabIndicator? parseUnderlineTabIndicator(
    dynamic value, ThemeData theme,
    [UnderlineTabIndicator? defaultValue]) {
  if (value == null) return defaultValue;
  return UnderlineTabIndicator(
    insets: parseEdgeInsets(value['insets'], EdgeInsets.zero)!,
    borderSide: parseBorderSide(value['border_side'], theme,
        defaultValue: const BorderSide(width: 2.0, color: Colors.white))!,
    borderRadius: parseBorderRadius(value['border_radius']),
  );
}

extension TabParsers on Control {
  TabBarIndicatorSize? getTabBarIndicatorSize(String propertyName,
      [TabBarIndicatorSize? defaultValue]) {
    return parseTabBarIndicatorSize(get(propertyName), defaultValue);
  }

  TabIndicatorAnimation? getTabIndicatorAnimation(String propertyName,
      [TabIndicatorAnimation? defaultValue]) {
    return parseTabIndicatorAnimation(get(propertyName), defaultValue);
  }

  UnderlineTabIndicator? getUnderlineTabIndicator(
      String propertyName, ThemeData theme,
      [UnderlineTabIndicator? defaultValue]) {
    return parseUnderlineTabIndicator(get(propertyName), theme, defaultValue);
  }
}
