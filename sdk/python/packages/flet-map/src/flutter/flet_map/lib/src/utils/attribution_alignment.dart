import 'package:flet/flet.dart';
import 'package:flutter_map/flutter_map.dart';

AttributionAlignment? parseAttributionAlignment(String? value,
    [AttributionAlignment? defaultValue]) {
  return parseEnum(AttributionAlignment.values, value, defaultValue);
}

extension AttributionAlignmentControlExtension on Control {
  AttributionAlignment? getAttributionAlignment(String propertyName,
      [AttributionAlignment? defaultValue]) {
    return parseAttributionAlignment(getString(propertyName), defaultValue);
  }
}
