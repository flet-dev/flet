import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'webview_mobile_and_mac.dart';
import 'webview_web.dart' if (dart.library.io) "webview_web_vain.dart";
// `dart.library.html` is undefined under dart2wasm, so keying on it selected
// the native implementation for `flutter build web --wasm`. `dart.library.io`
// is false on both dart2js and dart2wasm, so it is the only key that actually
// separates web from native — which is why the stub is the default branch here.
import 'webview_windows_and_linux_vain.dart'
    if (dart.library.io) 'webview_windows_and_linux.dart';

class WebViewControl extends StatelessWidget {
  final Control control;

  const WebViewControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("WebViewControl build: ${control.id}");
    Widget view =
        const ErrorControl("Webview is not yet supported on this platform.");
    if (isWebPlatform()) {
      view = WebviewWeb(control: control);
    } else if (isMobilePlatform() || isMacOSDesktop()) {
      view = WebviewMobileAndMac(control: control);
    } else if (isWindowsDesktop() || isLinuxDesktop()) {
      view = WebviewDesktop(control: control);
    }

    return LayoutControl(control: control, child: view);
  }
}
