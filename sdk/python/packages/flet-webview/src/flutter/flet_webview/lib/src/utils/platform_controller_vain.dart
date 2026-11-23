import 'package:webview_all/webview_all.dart';

/// Web stubs for `platform_controller.dart`.
///
/// The Android, Windows and Linux implementation packages import `dart:io`,
/// so they are swapped out on dart2js and dart2wasm.
PlatformWebViewControllerCreationParams createPlatformCreationParams() =>
    const PlatformWebViewControllerCreationParams();

Future<void> allowFileAccess(WebViewController controller) async {}

Future<void> loadLocalFile(
  WebViewController controller,
  String absoluteFilePath,
) => controller.loadFile(absoluteFilePath);

/// Closes the iframe session behind [controller]: its window message
/// listener, pending requests and document observers.
Future<void> disposePlatformController(WebViewController controller) =>
    controller.platform.closeWebViewSession();
