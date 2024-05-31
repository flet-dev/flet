import "package:collection/collection.dart";
import "package:flet/flet.dart";
import "package:permission_handler/permission_handler.dart";

Permission? parsePermission(String? permission,
    [Permission? defaultPermission]) {
  if (permission == null) {
    return defaultPermission;
  }
  return Permission.values.firstWhereOrNull(
        (Permission p) =>
            trimStart(p.toString().toLowerCase(), "permission.") ==
            permission.toLowerCase(),
      ) ??
      defaultPermission;
}
