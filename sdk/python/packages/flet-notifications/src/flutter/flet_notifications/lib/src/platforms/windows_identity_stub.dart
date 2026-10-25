import 'windows_identity.dart';

/// The default [WindowsIdentity] of the running app, from its version
/// information and executable.
Future<WindowsIdentity> defaultWindowsIdentity() async =>
    windowsIdentity(productName: "", internalName: "", executablePath: "");
