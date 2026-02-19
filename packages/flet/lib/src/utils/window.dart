import 'package:window_manager/window_manager.dart';
import 'enums.dart';

import '../models/control.dart';

ResizeEdge? parseWindowResizeEdge(String? value, [ResizeEdge? defaultValue]) {
  return parseEnum(ResizeEdge.values, value, defaultValue);
}

extension WindowParsers on Control {
  ResizeEdge? getWindowResizeEdge(String propertyName,
      [ResizeEdge? defaultValue]) {
    return parseWindowResizeEdge(get(propertyName), defaultValue);
  }
}
