import 'dart:convert';

import 'package:crypto/crypto.dart';

export 'windows_identity_stub.dart'
    if (dart.library.io) 'windows_identity_io.dart';

/// How Windows identifies the app's notifications.
///
/// Windows keys notification settings, history and toast activation on these
/// values, so apps must not share them.
typedef WindowsIdentity = ({
  String appName,
  String appUserModelId,
  String guid,
});

/// Namespace of the GUIDs derived by [windowsIdentity].
const String _guidNamespace = "c8b28b8a-5d47-46ee-b461-e128fa3932c2";

/// Derives an app's default [WindowsIdentity] from its executable.
///
/// The AppUserModelID combines [internalName] with a hash of
/// [executablePath], so it is stable across launches and differs between
/// apps, and between copies of an app installed in different places. The GUID
/// is a name-based UUID of the AppUserModelID.
WindowsIdentity windowsIdentity({
  required String productName,
  required String internalName,
  required String executablePath,
}) {
  final name = internalName.replaceAll(RegExp(r"[^A-Za-z0-9]"), "");
  final pathHash = sha1
      .convert(utf8.encode(executablePath.toLowerCase()))
      .toString()
      .substring(0, 8);
  final appUserModelId =
      "Flet.${name.isEmpty ? "App" : name.substring(0, name.length.clamp(0, 64))}"
      ".$pathHash";
  return (
    appName: productName.trim().isEmpty ? "Flet App" : productName.trim(),
    appUserModelId: appUserModelId,
    guid: _uuid5(_guidNamespace, appUserModelId),
  );
}

/// A name-based UUID, version 5, as defined by RFC 9562.
String _uuid5(String namespace, String name) {
  final namespaceBytes = [
    for (var i = 0; i < 32; i += 2)
      int.parse(namespace.replaceAll("-", "").substring(i, i + 2), radix: 16),
  ];
  final bytes = sha1
      .convert([...namespaceBytes, ...utf8.encode(name)])
      .bytes
      .sublist(0, 16);
  bytes[6] = (bytes[6] & 0x0f) | 0x50;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  final hex = bytes.map((b) => b.toRadixString(16).padLeft(2, "0")).join();
  return "${hex.substring(0, 8)}-${hex.substring(8, 12)}-"
      "${hex.substring(12, 16)}-${hex.substring(16, 20)}-${hex.substring(20)}";
}
