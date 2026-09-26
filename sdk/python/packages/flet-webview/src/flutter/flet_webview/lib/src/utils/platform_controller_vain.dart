import 'package:webview_all/webview_all.dart';

/// Web stubs for `platform_controller.dart`.
///
/// The Android, Windows and Linux implementation packages import `dart:io`,
/// so they are swapped out on dart2js and dart2wasm.
PlatformWebViewControllerCreationParams createPlatformCreationParams() =>
    const PlatformWebViewControllerCreationParams();

Future<void> allowFileAccess(WebViewController controller) async {}

Future<void> disposePlatformController(WebViewController controller) async {}
