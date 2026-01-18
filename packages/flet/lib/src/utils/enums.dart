import 'package:collection/collection.dart';

T? parseEnum<T extends Enum>(List<T> values, String? value, [T? defaultValue]) {
  if (value == null) return defaultValue;

  return values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}
