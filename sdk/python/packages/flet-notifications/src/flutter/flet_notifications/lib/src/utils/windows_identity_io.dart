import 'dart:io';

import 'package:flutter/foundation.dart' show debugPrint;
import 'package:package_info_plus/package_info_plus.dart';

import 'windows_identity.dart';

/// The default [WindowsIdentity] of the running app, from its version
/// information and executable, or from the executable alone when the version
/// information can't be read.
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
  return windowsIdentity(
    productName: productName,
    internalName: internalName,
    executablePath: Platform.resolvedExecutable,
  );
}
