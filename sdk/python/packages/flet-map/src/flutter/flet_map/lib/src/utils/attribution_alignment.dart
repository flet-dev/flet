import 'package:collection/collection.dart';
import 'package:flutter_map/flutter_map.dart';

AttributionAlignment? parseAttributionAlignment(String? value,
    [AttributionAlignment? defValue]) {
  if (value == null) return defValue;
  return AttributionAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}
