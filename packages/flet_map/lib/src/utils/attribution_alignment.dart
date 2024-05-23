import 'package:flet/flet.dart';
import 'package:flutter_map/flutter_map.dart';

AttributionAlignment? parseAttributionAlignment(
    String propName, Control control,
    [AttributionAlignment? defaultAlignment]) {
  String? a = control.attrString(propName);
  switch (a?.toLowerCase()) {
    case "bottomleft":
      return AttributionAlignment.bottomLeft;
    case "bottomright":
      return AttributionAlignment.bottomRight;
    default:
      return defaultAlignment;
  }
}
