import "package:collection/collection.dart";
import "package:permission_handler/permission_handler.dart";

Permission? parsePermission(String? value, [Permission? defaultValue]) {
  if (value == null) return defaultValue;
  return Permission.values.firstWhereOrNull(
        (Permission p) =>
            p.toString().split('.').last.toLowerCase() == value.toLowerCase(),
      ) ??
      defaultValue;
}
