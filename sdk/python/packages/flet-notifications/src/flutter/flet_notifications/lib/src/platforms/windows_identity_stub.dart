import 'windows_identity.dart';

/// The default [WindowsIdentity] of the running app, from its version
/// information and executable.
Future<WindowsIdentity> defaultWindowsIdentity() async =>
    windowsIdentity(productName: "", internalName: "", executablePath: "");

/// The executable Windows can start to deliver a notification selection made
/// after the app exited, or `null` when there is none.
String? windowsLauncherPath() => null;

/// Registers [executable] as the server of the COM class [guid]; returns
/// whether the entry was written.
bool registerWindowsLauncher(String guid, String executable) => false;
