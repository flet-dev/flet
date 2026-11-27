import 'package:webview_all/webview_all.dart';
import 'package:webview_all_web/webview_all_web.dart';

/// Web stubs for `platform_controller.dart`.
///
/// The Android, Windows and Linux implementation packages import `dart:io`,
/// so they are swapped out on dart2js and dart2wasm.

/// What a [sandboxed] frame may do: run scripts, submit forms, open popups
/// and show dialogs - not use its real origin, and not navigate the page.
const _sandbox =
    "allow-scripts allow-forms allow-popups "
    "allow-popups-to-escape-sandbox allow-modals allow-downloads "
    "allow-presentation";

/// Creation params for the web `<iframe>`.
///
/// A [sandboxed] frame runs whatever it shows, even a page from the app's own
/// site or HTML loaded with `loadHtmlString`, with an opaque origin, apart
/// from the page around it. `webview_all_web` then reaches the HTML it loads
/// through its message bridge.
PlatformWebViewControllerCreationParams createPlatformCreationParams({
  bool sandboxed = false,
}) => sandboxed
    ? WebWebViewControllerCreationParams(iFrameSandbox: _sandbox)
    : const PlatformWebViewControllerCreationParams();

Future<void> allowFileAccess(WebViewController controller) async {}

Future<void> loadLocalFile(
  WebViewController controller,
  String absoluteFilePath,
) => controller.loadFile(absoluteFilePath);

/// Closes the iframe session behind [controller]: its window message
/// listener, pending requests and document observers.
Future<void> disposePlatformController(WebViewController controller) =>
    controller.platform.closeWebViewSession();
