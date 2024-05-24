import "package:collection/collection.dart";
import "package:permission_handler/permission_handler.dart";

Permission? parsePermission(String? permission,
    [Permission? defaultPermission]) {
  return Permission.values.firstWhereOrNull(
        (Permission p) =>
            p.toString().toLowerCase() == permission?.toLowerCase(),
      ) ??
      defaultPermission;
}
