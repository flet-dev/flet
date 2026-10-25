import 'dart:io';

import 'package:flutter/foundation.dart' show debugPrint;
import 'package:package_info_plus/package_info_plus.dart';

import 'windows_identity.dart';

/// The default [WindowsIdentity] of the running app, from its version
/// information and executable, or from the executable alone when the version
/// information can't be read.
///
/// An app packaged with `flet pack` runs the shared Flet client, so its
/// identity is derived from the packaged executable, which the app passes in
/// `FLET_APP_USER_MODEL_ID`.
///
/// The icon is the `data\app_icon.ico` that `flet build` places next to the
/// executable, when present.
Future<WindowsIdentity> defaultWindowsIdentity() async {
  var productName = "";
  var internalName = "";
  try {
    final info = await PackageInfo.fromPlatform();
    productName = info.appName;
    internalName = info.packageName;
  } catch (e) {
    debugPrint("flet_notifications: reading the app's version info failed: $e");
  }
  final executable = File(Platform.resolvedExecutable);
  final icon = File("${executable.parent.path}\\data\\app_icon.ico");
  return windowsIdentity(
    productName: productName,
    internalName: internalName,
    executablePath:
        Platform.environment["FLET_APP_USER_MODEL_ID"] ?? executable.path,
    iconPath: icon.existsSync() ? icon.path : null,
  );
}
