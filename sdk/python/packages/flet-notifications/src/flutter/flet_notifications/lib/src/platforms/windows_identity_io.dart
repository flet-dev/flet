import 'dart:ffi';
import 'dart:io';

import 'package:ffi/ffi.dart';
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

/// The executable Windows can start to deliver a notification selection made
/// after the app exited, or `null` when there is none.
///
/// Only a `flet build` app runs on its own: it ships its Python runtime next to
/// its executable. The Flet client of `flet run` and `flet pack` needs Python
/// to start it with the app.
String? windowsLauncherPath() {
  final executable = File(Platform.resolvedExecutable);
  final runtime =
      File("${executable.parent.path}\\serious_python_windows_plugin.dll");
  return runtime.existsSync() ? executable.path : null;
}

/// Registers [executable] as the server of the COM class [guid], for the
/// current user.
///
/// Windows delivers notification selections by activating that class. The
/// notifications plugin registers it only inside the running app, so once the
/// app exits, Windows has nothing to start. This entry lets Windows start the
/// app, which then receives the selection once it registers the class.
///
/// Returns whether the entry was written.
bool registerWindowsLauncher(String guid, String executable) {
  final subKey =
      "Software\\Classes\\CLSID\\{$guid}\\LocalServer32".toNativeUtf16();
  final command = '"$executable"';
  final value = command.toNativeUtf16();
  try {
    return _regSetKeyValue(_hkeyCurrentUser, subKey, nullptr, _regSz,
            value.cast(), (command.length + 1) * sizeOf<Uint16>()) ==
        0;
  } finally {
    malloc.free(subKey);
    malloc.free(value);
  }
}

/// `HKEY_CURRENT_USER`, a sign-extended 32-bit handle.
const int _hkeyCurrentUser = -0x7fffffff;

/// `REG_SZ`, a null-terminated string value.
const int _regSz = 1;

final _regSetKeyValue = DynamicLibrary.open("advapi32.dll").lookupFunction<
    Int32 Function(IntPtr hKey, Pointer<Utf16> subKey, Pointer<Utf16> valueName,
        Uint32 type, Pointer<Void> data, Uint32 dataSize),
    int Function(int hKey, Pointer<Utf16> subKey, Pointer<Utf16> valueName,
        int type, Pointer<Void> data, int dataSize)>("RegSetKeyValueW");
