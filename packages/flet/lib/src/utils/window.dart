import 'package:collection/collection.dart';
import 'package:window_manager/window_manager.dart';

import '../models/control.dart';

ResizeEdge? parseWindowResizeEdge(String? value, [ResizeEdge? defaultValue]) {
  if (value == null) return defaultValue;
  return ResizeEdge.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

extension WindowParsers on Control {
  ResizeEdge? getWindowResizeEdge(String propertyName,
      [ResizeEdge? defaultValue]) {
    return parseWindowResizeEdge(get(propertyName), defaultValue);
  }
}
